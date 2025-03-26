import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;

public class ImageFormatChecker {
    private static final List<String> SUPPORTED_FORMATS = Arrays.asList("jpeg", "png", "gif", "bmp", "tiff");

    public static String getImageFormat(String imagePath) throws IOException {
        File file = new File(imagePath);
        BufferedImage image = ImageIO.read(file);
        
        if (image == null) {
            throw new IOException("Unsupported image format or corrupted file: " + imagePath);
        }

        String formatName = getFormatName(file);
        if (!SUPPORTED_FORMATS.contains(formatName.toLowerCase())) {
            throw new IllegalArgumentException("Unsupported image format: " + formatName);
        }
        return formatName;
    }

    private static String getFormatName(File file) throws IOException {
        String format = ImageIO.getImageReaders(ImageIO.createImageInputStream(file)).next().getFormatName();
        return format.toLowerCase();
    }

    public static void main(String[] args) {
        try {
            String format = getImageFormat("card.png");
            System.out.println("Image format: " + format);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}

