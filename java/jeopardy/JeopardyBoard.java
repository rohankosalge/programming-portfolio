package jeopardy;
/*
 * Programmer: Rohan Kosalge
 * 
 * Date: (First Day) March 25th, 2020
 * 		 (Last Update) May 1st, 2020
 * 
 * Purpose: This is the panel that shows the whole board, with the list of categories and questions and stuff.
 * 			It also has a whole list of setters and getters, all used for the answer panel. It's pretty
 * 			self-explanatory at first, but there are some other things.
 *
 */

// import java.awt and java.event for listeners 
// import javax.swing for UI
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

// this extends the parent class, so I get access to it's stuff.
public class JeopardyBoard extends Jeopardy3 {
	
	// a 75% me, 25% Stack Overflow made class for text formatting.
	// g.drawString() doesn't have good centering within a rect, so why not flex my coding skills?
	// And YES, I've tried text areas and text panes. There are always errors.
	TextFormat textFormat = new TextFormat();
	
	// funny named variable, but really does stop "widget corruption"!
	// this simple switch just controls the repetition that may occur.
	// a widget that has already been put on the board may be put again, so the switch stops it.
	boolean stopCorruption = false;
	
	// constant fonts.
	static final Font BOARD_FONT = new Font("Impact", Font.BOLD, 40);
	static final Font CAT_FONT = new Font("Impact", Font.BOLD, 20);
	static final Font POINTS_FONT = new Font("Impact", Font.BOLD, 50);
	
	// whole list of variables used here.
	/*
	 * USER ATTEMPTED KEY:
	 * 		null - user has not clicked on question.
	 * 		true - user clicked on question, got it right (+= point value)
	 * 		false - user clicked on question, got it right (-= point value)
	 */
	
	Boolean[][] userAttempted = new Boolean[5][7];
	
	// initializing JQuestion properties that are projected in the answer panel.
	String question = "question"; 
	String answer = "answer";
	String category = "category"; 
	int value = 0;
	
	// coordinates of the question, grid-wise. Used to locate question that user 
	// either located/answered.
	int bpx = 0; 
	int bpy = 0;	
	
	// make boolean to stop copying cat label on panel every certain fps.
	boolean stopCatRep = false;
	
	// pass cl, cards, and the list of questions
	public JeopardyBoard(CardLayout cl, JPanel cards, JQuestion[][] fuqs) {
		this.cl = cl;
		this.cards = cards;
		this.finalizedUserQuestions = fuqs;	
	}
	
	// the whole list of setters and getters for the above variables.
	// my parents (who are fortunately experts in Java) showed me how to easily
	// make setters and getters for variables using the Eclipse IDE.
	public boolean getStopCorruption() {
		return stopCorruption;
	}
	
	public void setStopCorruption(boolean sc) {
		stopCorruption = sc;
	}

	
	
	public Boolean[][] getUser_attempted() {
		return userAttempted;
	}

	public void setUserAttempted(boolean attempt) {
		this.userAttempted[bpx][bpy] = attempt;
	}

	public String getQuestion() {
		return question;
	}

	public void setQuestion(String question) {
		this.question = question;
	}

	public String getAnswer() {
		return answer;
	}

	public void setAnswer(String answer) {
		this.answer = answer;
	}

	public String getCategory() {
		return category;
	}

	public void setCategory(String category) {
		this.category = category;
	}

	public int getValue() {
		return value;
	}

	public void setValue(int value) {
		this.value = value;
	}

	public int getBpx() {
		return bpx;
	}

	public void setBpx(int bpx) {
		this.bpx = bpx;
	}

	public int getBpy() {
		return bpy;
	}

	public void setBpy(int bpy) {
		this.bpy = bpy;
	}
	
	// used in answer panel, to add or subtract points.
	public void addPoints() {
		Jeopardy3.points += value;
	}
	
	public void subtractPoints() {
		Jeopardy3.points -= value;
	}
	
	// not at all similar to stopCorruption! 
	// since my widgets are actually in paint component, there is some sort of FPS
	// and the same widgets are constantly getting added at some rate.
	// this boolean stops the spam. So maybe I should change the naming...
	boolean stopRepeating = false;
	
	
	// I know, I know, I shouldn't be doing this in paintComponent....
	// I don't have a good reason to be doing this as well.
	public void paintComponent(Graphics g) {
		
		
		super.paintComponent(g);
		
		// draw board. I use userAttempted to color code the grid.
		
		// a small key:
		/* 
		 * BLUE - null
		 * GREEN - correct
		 * RED - wrong
		 * 
		 * And not gonna lie, the default colors are ugly! After all, "red" is #ff0000
		 * and green is #00ff00. But I like the blue. I made use of hex codes here.
		 */
		
		g.setColor(Color.BLUE);
		
		g.setFont(BOARD_FONT);
		for(int x=0; x<7; x++) {			
			for(int y=0; y<6; y++) {
				g.setColor(Color.BLUE);
				if(y>0) {
					if(userAttempted[y-1][x] !=null) {
						if(userAttempted[y-1][x] ==true) {
							g.setColor(Color.decode("#07a824"));
						}else {
							g.setColor(Color.decode("#db1b00"));
						}
					}
				}
				
				
				g.fillRect(150*x, 100*y, 150, 100);
				
				// check for positioning and draw the numbers, from $200 to $1000.
				// I use orange for everything, it looks gold with the blue behind it.
				if(y>0) {
					g.setColor(Color.ORANGE);
					textFormat.drawCenteredLine(g, "$"+Integer.toString(200*y), (150*x), (100*y), 150, 100, BOARD_FONT);
					//g.drawString(Integer.toString(200*y), (150*x)+45, (100*y)+65);
				}
			}
		}
		
		g.setColor(Color.BLUE);
		g.fillRect(0, 600, 1050, 100);
		
		// draw the grid lines here. I do it after the board drawing because 
		// the rectangles actually cover the lines. Like, really?!
		g.setColor(Color.BLACK);
		for(int x=0; x<8; x++) {
			g.drawLine(150*x, 0, 150*x, 600);
			g.drawLine(0, 100*x, 1050, 100*x);
		}
		
		g.setColor(Color.ORANGE);
		
		// the bottom box, write the points down.
		String pointsText = "POINTS: " + points;
		textFormat.drawCenteredLine(g, pointsText, 0, 600, 1050, 100, POINTS_FONT);
		
		
		g.setColor(Color.WHITE);
		
		// still a work in progress. The one constant issue this entire time.
		// this should draw the category titles at the top of the board, but
		// the formatting is really off. I don't know what the error is, but I gotta find it.
		
		setLayout(null);
		if(stopCatRep==false) {
			for(int x=0; x<7; x++) { 
				String cat = finalizedUserQuestions[x][0].getCat();

				JTextArea catTextArea = new JTextArea(cat);
				
				catTextArea.setBounds((150*x)+20, 10, 110, 80);
				catTextArea.setAlignmentX(CENTER_ALIGNMENT);
				catTextArea.setAlignmentY(CENTER_ALIGNMENT);
				catTextArea.setEditable(false);
				catTextArea.setLineWrap(true);
				catTextArea.setWrapStyleWord(true);
				catTextArea.setBackground(Color.BLUE);
				catTextArea.setForeground(Color.WHITE);
				catTextArea.setFont(CAT_FONT);
				
				add(catTextArea);
				
			stopCatRep = true;
		}
		
			
			//textFormat.drawCenteredText(cat, getFontMetrics(CAT_FONT), g, CAT_FONT,
			 // 150*x, 0, (150*x)+150, 100); 
		}		
	}
	
	// check mouse input, show answerpanel if mouse click bounds
	// are in the board. The values of the corresponding JQuestion are passed.
	public void mouseClicked(MouseEvent e) {
		stopCorruption = false;
		
		int x = e.getX(); int y = e.getY();
		int q; int cat;
		
		// formulas with regards to Stack Overflow. Used to "round" to the
		// right finalizedUserQuestions coordinates.
		q = ((y+99)/100)-2;
		cat = ((x+149)/150)-1;		
		
		// check if boundaries are valid, then switch to answer panel
		// and pass the values.
		if((q>=0 && q<=4)){
			
			// find the corresponding JQuestion based on the coordinates.
			JQuestion qu = finalizedUserQuestions[cat][q];
		
			// set values to the main variables, then switch.
			this.setQuestion(qu.getQ());
			this.setAnswer(qu.getA());
			this.setCategory(qu.getCat());
			this.setValue(qu.getVal());
			this.setBpx(q);
			this.setBpy(cat);
			
			cl.show(cards, "Jeopardy! Answer");
			back.setEnabled(false);
			
		}
	}

	// useless methods that just take up space.
	public void mousePressed(MouseEvent e) {
	}
	public void mouseReleased(MouseEvent e) {
	}
	public void mouseEntered(MouseEvent e) {
	}
	public void mouseExited(MouseEvent e) {
	}
	public void actionPerformed(ActionEvent e) {
		removeAll();
		repaint();
	}
}
