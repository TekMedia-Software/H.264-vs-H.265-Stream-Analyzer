# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial release of the project with basic video comparison functionalities.
- Support for H.264 and H.265 video file inputs.
- Display of PSNR, SSIM, and VMAF metrics for video quality evaluation.
- Play, pause, stop and seek controls for video playback.
- Basic user interface with PyQt5 for loading and analyzing videos.
- Added graphical comparison feature and the ability to save H.264 vs H.265 analysis results to a file for future reference.

### Changed
- Enhanced UI for a more user-friendly experience.
- Improved analysis speed by optimizing FFmpeg command execution.

### Deprecated
- No deprecated features yet.

### Removed
- No features removed.

### Fixed
- Resolved lag issue when loading multiple videos.
- Fixed minor UI misalignment on smaller screens.

### Security
- No security-related changes yet.

---

## [Version 1.0.1] - 2024-10-21

### Added
  **Initial release** of the project with support for:
- Results box to display PSNR, SSIM, and VMAF scores for H.264 and H.265 analysis.
- Graphical comparison of video metrics with side-by-side bar charts for H.264 and H.265.
- User controls for loading reference, H.264, and H.265 videos.
- Sync window, frame rate, and thread input options for customizable analysis.

### Changed
- UI Refinements: Improved the layout and spacing of the interface for better clarity and ease of use.

### Deprecated
- No deprecated features.

### Fixed
- UI Bug Fixes: Fixed minor layout issues, such as button alignment and spacing.

### Security
- No security-related changes yet.
