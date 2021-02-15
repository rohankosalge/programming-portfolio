package jeopardy;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;

public class TextFormat {
	public TextFormat() {
		
	}
	
	public void drawCenteredLine(Graphics g, String text, int rx, int ry, int rw, int rh, Font font) {
		FontMetrics metrics = g.getFontMetrics(font);
		int x = rx + (rw-metrics.stringWidth(text))/2;
		int y = ry + ((rh-metrics.getHeight())/2)+metrics.getAscent();
		g.setFont(font);
		g.drawString(text, x, y);
	}
	
	public void drawCenteredText(String text, FontMetrics textMetrics, Graphics g, Font font, int x, int y, int lim, int rh) {
		int lineHeight = textMetrics.getHeight();
		String t = text;
		String[] arr = t.split("\\s+");
		int nIndex = 0;
		int startX = x;
		int startY = y;
		while(nIndex < arr.length) {
			String line = arr[nIndex++];
			while((nIndex<arr.length)&&(textMetrics.stringWidth(line+" "+arr[nIndex])<lim)) {
				line = line + " " + arr[nIndex];
				nIndex++;
			}
			
			drawCenteredLine(g, line, startX, startY, lim-startX, rh, font);
			//g.drawString(line, startX, startY);
			startY+=lineHeight;
		}
	}
	
}
