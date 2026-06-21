"""
utils/image_filters.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Image preprocessing pipeline for Traffic Netra.
Handles low-light, blur, contrast normalisation, and rain/fog.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import cv2
import numpy as np
from typing import Optional


class ImagePreprocessor:
    """
    Applies a configurable chain of image enhancement filters
    to improve YOLO detection accuracy under adverse conditions.
    """

    def enhance(
        self,
        image: np.ndarray,
        clahe:    bool = True,
        deblur:   bool = False,
        contrast: bool = True,
        denoise:  bool = False,
    ) -> np.ndarray:
        """
        Main enhancement pipeline.  Processes in LAB colour space
        to avoid hue shifts during luminance adjustments.

        Args:
            image:    RGB numpy array
            clahe:    Apply CLAHE contrast limited adaptive histogram eq.
            deblur:   Apply Wiener-inspired unsharp mask deblur.
            contrast: Apply auto white-balance / contrast stretch.
            denoise:  Apply Non-local Means denoising (slow on CPU).

        Returns:
            Enhanced RGB numpy array, same shape as input.
        """
        if image is None or image.size == 0:
            return image

        result = image.copy().astype(np.uint8)

        # ── Denoise first (reduces CLAHE artefacts) ────────────────────────
        if denoise:
            result = self._denoise(result)

        # ── Auto contrast stretch ──────────────────────────────────────────
        if contrast:
            result = self._auto_contrast(result)

        # ── CLAHE on luminance ─────────────────────────────────────────────
        if clahe:
            result = self._apply_clahe(result)

        # ── Deblur / sharpening ────────────────────────────────────────────
        if deblur:
            result = self._deblur(result)

        return result

    # ── Individual Filter Implementations ─────────────────────────────────────

    def _apply_clahe(self, image: np.ndarray) -> np.ndarray:
        """
        Contrast Limited Adaptive Histogram Equalisation applied only
        to the L channel in LAB colour space.
        """
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l_eq  = clahe.apply(l)

        lab_eq = cv2.merge([l_eq, a, b])
        return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2RGB)

    def _auto_contrast(self, image: np.ndarray) -> np.ndarray:
        """
        Per-channel histogram stretch (Percentile-based) to handle
        both over- and under-exposed images.
        """
        result = np.zeros_like(image)
        for i in range(3):
            channel = image[:, :, i]
            p_low   = np.percentile(channel, 1)
            p_high  = np.percentile(channel, 99)
            if p_high - p_low < 10:
                result[:, :, i] = channel
                continue
            stretched = (channel.astype(np.float32) - p_low) / (p_high - p_low) * 255
            result[:, :, i] = np.clip(stretched, 0, 255).astype(np.uint8)
        return result

    def _deblur(self, image: np.ndarray) -> np.ndarray:
        """
        Unsharp mask for motion / defocus blur correction.
        Sigma tuned for traffic camera blur profiles (~2-3px motion).
        """
        blurred  = cv2.GaussianBlur(image, (0, 0), sigmaX=2.0)
        sharpened = cv2.addWeighted(image, 1.6, blurred, -0.6, 0)
        return np.clip(sharpened, 0, 255).astype(np.uint8)

    def _denoise(self, image: np.ndarray) -> np.ndarray:
        """
        Non-local Means denoising — effective for nighttime grain.
        Note: can be slow (~0.5-2s) on large images.
        """
        bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        denoised_bgr = cv2.fastNlMeansDenoisingColored(
            bgr,
            None, h=8, hColor=8,
            templateWindowSize=7, searchWindowSize=21,
        )
        return cv2.cvtColor(denoised_bgr, cv2.COLOR_BGR2RGB)

    def _night_enhance(self, image: np.ndarray) -> np.ndarray:
        """
        Gamma correction for night / severely underexposed frames.
        Uses adaptive gamma based on mean luminance.
        """
        gray   = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        mean_l = np.mean(gray)

        if mean_l > 80:
            return image   # not night scene

        # Gamma = log(0.5) / log(mean_L / 255)
        gamma   = np.log(0.5) / np.log(max(mean_l, 1) / 255.0)
        gamma   = np.clip(gamma, 0.4, 3.0)

        inv_g   = 1.0 / gamma
        table   = np.array([
            min(255, int((i / 255.0) ** inv_g * 255))
            for i in range(256)
        ], np.uint8)

        return cv2.LUT(image, table)

    def assess_quality(self, image: np.ndarray) -> dict:
        """
        Compute image quality metrics to inform filter selection.
        Returns dict with brightness, blur_score, noise_estimate.
        """
        gray         = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        brightness   = float(np.mean(gray))
        blur_score   = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        noise_est    = float(np.std(gray.astype(np.float32) -
                                    cv2.GaussianBlur(gray, (5,5), 0).astype(np.float32)))
        return {
            "brightness":    brightness,          # 0–255
            "blur_score":    blur_score,           # higher = sharper
            "noise_estimate": noise_est,           # lower = cleaner
            "is_dark":       brightness < 60,
            "is_blurry":     blur_score < 100,
            "is_noisy":      noise_est > 12,
        }

    def auto_enhance(self, image: np.ndarray) -> np.ndarray:
        """
        Quality-aware auto-enhancement: assesses the image and applies
        only the filters that are actually needed.
        """
        quality = self.assess_quality(image)
        return self.enhance(
            image,
            clahe    = quality["is_dark"] or quality["noise_estimate"] > 8,
            deblur   = quality["is_blurry"],
            contrast = True,
            denoise  = quality["is_noisy"],
        )
