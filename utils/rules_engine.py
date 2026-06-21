"""
utils/rules_engine.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Logical breach checking engine for Traffic Netra.
Takes raw YOLO detections and applies geometric + class rules
to classify traffic violations with confidence scores.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import numpy as np
from typing import List, Dict, Optional, Tuple

# ─── Legal Section References ─────────────────────────────────────────────────
LEGAL_SECTIONS = {
    "Triple Riding":       {
        "section": "Section 128, Motor Vehicles Act 1988",
        "penalty": "Rs. 2,000 or imprisonment up to 3 months",
        "description": (
            "Three or more persons were detected riding on a single two-wheeled motor vehicle. "
            "The Motor Vehicles Act strictly prohibits more than two persons on a motorcycle. "
            "Rider count exceeded permissible limit."
        ),
    },
    "No Helmet":           {
        "section": "Section 129, Motor Vehicles Act 1988",
        "penalty": "Rs. 1,000 (first offence); Rs. 2,000 (repeat) + licence suspension",
        "description": (
            "Rider on a two-wheeler detected without a protective helmet. "
            "Wearing a BIS-certified helmet is mandatory for all riders "
            "and pillion passengers under Section 129 of the MV Act."
        ),
    },
    "Stop Line Violation": {
        "section": "Section 122, Motor Vehicles Act 1988",
        "penalty": "Rs. 500 (two-wheeler) / Rs. 1,000 (four-wheeler)",
        "description": (
            "Vehicle front axle detected beyond the marked stop line. "
            "Drivers must stop before the stop line at all red signals "
            "and pedestrian crossings as mandated by traffic regulations."
        ),
    },
    "Illegal Parking":     {
        "section": "Section 122(1), Motor Vehicles Act 1988",
        "penalty": "Rs. 500 (Light vehicle) / Rs. 1,500 (Heavy vehicle)",
        "description": (
            "Vehicle stationary within a designated no-parking zone or restricted area. "
            "Parking in prohibited zones impedes traffic flow and is a cognisable offence."
        ),
    },
    "Wrong-Side Driving":  {
        "section": "Section 112, Motor Vehicles Act 1988",
        "penalty": "Rs. 5,000 (first) / Rs. 10,000 (repeat)",
        "description": (
            "Vehicle detected travelling in the wrong lane or against the designated traffic direction. "
            "This constitutes a dangerous traffic violation with enhanced penalties."
        ),
    },
    "Red-Light Violation": {
        "section": "Section 119, Motor Vehicles Act 1988",
        "penalty": "Rs. 1,000 (first offence) / Rs. 5,000 (repeat)",
        "description": (
            "Vehicle crossed the intersection while the signal was displaying red. "
            "Jumping red signals is a serious violation endangering pedestrians and crossing vehicles."
        ),
    },
    "Seatbelt Compliance": {
        "section": "Section 194B, Motor Vehicles Act 1988",
        "penalty": "Rs. 1,000",
        "description": (
            "Vehicle occupant detected without seatbelt. Wearing a seatbelt is mandatory "
            "for all front-seat occupants and rear-seat occupants where available."
        ),
    },
}


class RulesEngine:
    """
    Evaluates a list of detections against traffic violation rules.
    Returns a list of confirmed violations with confidence, legal ref, and description.
    """

    def evaluate(
        self,
        detections: List[Dict],
        active_checks: Optional[Dict[str, bool]] = None,
    ) -> List[Dict]:
        """
        Main entry point. Returns sorted list of violations detected.
        """
        if active_checks is None:
            active_checks = {k: True for k in LEGAL_SECTIONS}

        violations = []

        # Index by class
        by_class = _index_by_class(detections)

        # ── Rule 1: Triple Riding ──────────────────────────────────────────
        if active_checks.get("Triple Riding"):
            vs = self._check_triple_riding(by_class)
            violations.extend(vs)

        # ── Rule 2: No Helmet ─────────────────────────────────────────────
        if active_checks.get("No Helmet"):
            vs = self._check_no_helmet(by_class)
            violations.extend(vs)

        # ── Rule 3: Stop Line Violation ───────────────────────────────────
        if active_checks.get("Stop Line Violation"):
            vs = self._check_stop_line(by_class)
            violations.extend(vs)

        # ── Rule 4: Illegal Parking ───────────────────────────────────────
        if active_checks.get("Illegal Parking"):
            vs = self._check_illegal_parking(by_class)
            violations.extend(vs)

        # Sort by confidence descending
        return sorted(violations, key=lambda x: x["confidence"], reverse=True)

    # ── Individual Rule Implementations ───────────────────────────────────────

    def _check_triple_riding(self, by_class: Dict) -> List[Dict]:
        """
        Triple riding check using spatial containment and scale matching 
        to prevent background/foreground ghosting in dense traffic.
        """
        motos   = by_class.get("motorcycle", [])
        persons = by_class.get("person", [])
        violations = []

        if not motos or len(persons) < 3:
            return violations

        for moto in motos:
            mx1, my1, mx2, my2 = moto["bbox"]
            m_height = max(1, my2 - my1)
            
            riders = []
            for p in persons:
                px1, py1, px2, py2 = p["bbox"]
                p_height = py2 - py1
                p_cx = (px1 + px2) / 2
                
                # Check 1: Is the person's horizontal center inside the bike's bounds?
                # (Expanded slightly by 10% to account for leaning)
                m_width = mx2 - mx1
                in_x_bounds = (mx1 - 0.1 * m_width) <= p_cx <= (mx2 + 0.1 * m_width)
                
                # Check 2: Scale check. Rider height should be relative to bike height
                # Prevents tiny background people from being assigned to foreground bikes
                valid_scale = 0.4 < (p_height / m_height) < 1.8
                
                if in_x_bounds and valid_scale:
                    riders.append(p)

            if len(riders) >= 3:
                # We found a bike with 3 valid riders!
                conf = _aggregate_conf([moto] + riders[:3])
                meta = LEGAL_SECTIONS["Triple Riding"]
                steps = [
                    ("Motorcycle Detected", True),
                ]
                for r_idx in range(min(len(riders), 3)):
                    steps.append((f"Rider {r_idx + 1} Detected", True))
                steps.append(("Occupancy Limit Exceeded (Permissible: 2)", False))
                violations.append({
                    "label":       "Triple Riding",
                    "confidence":  conf,
                    "rider_count": len(riders),
                    "reasoning_steps": steps,
                    "bbox":        moto["bbox"],
                    **meta,
                })

        return violations

    def _check_no_helmet(self, by_class: Dict) -> List[Dict]:
        """
        Helmet violation: a person on a motorcycle whose head region contains a no_helmet detection.
        """
        motos = by_class.get("motorcycle", [])
        persons = by_class.get("person", [])
        heads_no_helmet = by_class.get("no_helmet", [])
        violations = []

        if not motos or not persons or not heads_no_helmet:
            return violations

        # Find valid riders on motorcycles
        for moto in motos:
            mx1, my1, mx2, my2 = moto["bbox"]
            m_height = max(1, my2 - my1)
            m_width = max(1, mx2 - mx1)
            
            riders = []
            for p in persons:
                px1, py1, px2, py2 = p["bbox"]
                p_height = py2 - py1
                p_cx = (px1 + px2) / 2
                
                in_x_bounds = (mx1 - 0.1 * m_width) <= p_cx <= (mx2 + 0.1 * m_width)
                valid_scale = 0.4 < (p_height / m_height) < 1.8
                
                if in_x_bounds and valid_scale:
                    riders.append(p)

            # Check each rider for no_helmet
            for rider in riders:
                rx1, ry1, rx2, ry2 = rider["bbox"]
                
                # Check if there is a 'no_helmet' near the rider
                violating_head = None
                for nh in heads_no_helmet:
                    nh_x1, nh_y1, nh_x2, nh_y2 = nh["bbox"]
                    nh_cx = (nh_x1 + nh_x2) / 2
                    nh_cy = (nh_y1 + nh_y2) / 2
                    
                    # If head center is inside rider box (with a small margin on top)
                    if rx1 <= nh_cx <= rx2 and ry1 - 30 <= nh_cy <= ry2:
                        violating_head = nh
                        break
                
                if violating_head:
                    conf = _aggregate_conf([moto, rider, violating_head])
                    meta = LEGAL_SECTIONS["No Helmet"]
                    violations.append({
                        "label": "No Helmet",
                        "confidence": conf,
                        "reasoning_steps": [
                            ("Motorcycle Detected", True),
                            ("Rider Detected", True),
                            ("Protective Helmet Missing", False),
                        ],
                        "bbox": violating_head["bbox"],
                        **meta
                    })

        return violations

    def _check_stop_line(self, by_class: Dict) -> List[Dict]:
        """
        Stop-line violation: any vehicle bbox whose bottom edge
        is below (y > line_y) the detected stop line.
        """
        stop_lines = by_class.get("stop_line", [])
        vehicles   = (by_class.get("car", []) + by_class.get("motorcycle", []) +
                      by_class.get("truck", []) + by_class.get("bus", []))
        violations = []

        if not stop_lines or not vehicles:
            return violations

        for line in stop_lines:
            line_y = (line["bbox"][1] + line["bbox"][3]) // 2
            for veh in vehicles:
                veh_bottom = veh["bbox"][3]
                if veh_bottom > line_y:
                    conf = veh["confidence"] * 0.92
                    meta = LEGAL_SECTIONS["Stop Line Violation"]
                    violations.append({
                        "label": "Stop Line Violation",
                        "confidence": conf,
                        "reasoning_steps": [
                            ("Stop-Line Demarcation Found", True),
                            ("Vehicle Bounds Identified", True),
                            ("Vehicle Breached Stop-Line", False),
                        ],
                        "bbox": veh["bbox"],
                        **meta
                    })

        return violations

    def _check_illegal_parking(self, by_class: Dict) -> List[Dict]:
        """
        Illegal parking: vehicle detected inside a 'no_parking_zone' region
        with sufficient IoU overlap.
        """
        zones    = by_class.get("no_parking_zone", [])
        vehicles = (by_class.get("car", []) + by_class.get("motorcycle", []) +
                    by_class.get("truck", []) + by_class.get("bus", []))
        violations = []

        if not zones or not vehicles:
            return violations

        for zone in zones:
            for veh in vehicles:
                iou = _compute_iou(veh["bbox"], zone["bbox"])
                if iou > 0.25:
                    conf = veh["confidence"] * 0.90
                    meta = LEGAL_SECTIONS["Illegal Parking"]
                    violations.append({
                        "label": "Illegal Parking",
                        "confidence": conf,
                        "reasoning_steps": [
                            ("No-Parking Zone Identified", True),
                            ("Stationary Vehicle Detected", True),
                            ("Vehicle Inside Restricted Zone", False),
                        ],
                        "bbox": veh["bbox"],
                        **meta
                    })

        return violations


# ─── Geometric Utility Functions ──────────────────────────────────────────────

def _index_by_class(detections: List[Dict]) -> Dict[str, List[Dict]]:
    """Group detections by class label."""
    index: Dict[str, List] = {}
    for d in detections:
        cls = d["class"]
        index.setdefault(cls, []).append(d)
    return index


def _compute_iou(boxA: List[int], boxB: List[int]) -> float:
    """
    Intersection over Union for two bounding boxes [x1,y1,x2,y2].
    Returns float in [0, 1].
    """
    xA = max(boxA[0], boxB[0]); yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2]); yB = min(boxA[3], boxB[3])

    inter = max(0, xB - xA) * max(0, yB - yA)
    if inter == 0:
        return 0.0

    areaA = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
    areaB = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])

    return inter / float(areaA + areaB - inter)


def _vertical_overlap_ratio(boxA: List[int], boxB: List[int]) -> float:
    """
    Ratio of vertical span overlap to boxA height.
    Used to check if a person is positioned over a motorcycle vertically.
    """
    top    = max(boxA[1], boxB[1])
    bottom = min(boxA[3], boxB[3])
    overlap = max(0, bottom - top)
    height_A = max(1, boxA[3] - boxA[1])
    return overlap / height_A


def _aggregate_conf(detections: List[Dict]) -> float:
    """
    Violation confidence should be bottlenecked by the least confident 
    critical detection, not averaged.
    """
    if not detections:
        return 0.0
    # Return the minimum confidence, capped at 0.97
    min_conf = min(d["confidence"] for d in detections)
    return min(0.97, min_conf)