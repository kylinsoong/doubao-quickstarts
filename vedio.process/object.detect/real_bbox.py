
def compute_real_bbox(bbox_str, video_width, video_height):
        """
        Calculate real bounding box coordinates from thousandth-scale values
        and return as a space-separated string.

        Args:
            bbox_str (str): Bounding box string in format "x_min y_min x_max y_max"
            video_width (int): Original video width (e.g., 3840)
            video_height (int): Original video height (e.g., 2160)

        Returns:
            str: Real coordinates as "x_min y_min x_max y_max" string
        """
        # Parse the bbox string into individual components
        x_min, y_min, x_max, y_max = map(int, bbox_str.split())

        # Calculate real coordinates using thousandth scale conversion
        real_x_min = int(x_min * video_width / 1000)
        real_y_min = int(y_min * video_height / 1000)
        real_x_max = int(x_max * video_width / 1000)
        real_y_max = int(y_max * video_height / 1000)

        # Return as space-separated string
        return f"{real_x_min} {real_y_min} {real_x_max} {real_y_max}"
