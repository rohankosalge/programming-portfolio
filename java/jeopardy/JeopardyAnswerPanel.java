package jeopardy;
/*
 * Programmer: Rohan Kosalge
 * 
 * Date: (First Day) March 25th, 2020
 * 		 (Last Update) May 1st, 2020
 * 
 * Purpose: In the actual game, when the contestant asks Mr. Trebek for a question, the screen
 * 			turns its attention to the question and "zooms" in, showing only the question.
 * 
 * 			I decided to imitate that, but since this is user-interactive, I have the question text on the top, 
 * 			with a text field to answer, an answer button, and a pass button.
 *
 *			This was a little frustrating at first, but I got the hang of it and was able to properly link
 *			all my variables used in answerpanel to jeopardyboard, so that they could all be understood by the console.
 *			
 *			A very clean and simple look!
 */


// import java.awt and java.event for listeners 
// import javax.swing for UI
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;


public class JeopardyAnswerPanel extends Jeopardy3 {
	
	// same purpose as stopRepeating, just for answer panel.
	// I gave it a different name just to easily identify the two.
	boolean stopDuplicating = false;
	
	// object of my formatting class.
	TextFormat textFormat2 = new TextFormat();
	
	// a bunch of constant fonts here.
	// I realized how many fonts I needed. At first I thought I would only need one,
	// but for each widget there just had to be a new one.
	static final Font QUESTION_FONT = new Font("Serif", Font.BOLD, 50);
	static final Font INFO_FONT = new Font("Serif", Font.PLAIN, 35);
	static final Font TYPE_FONT = new Font("Serif",Font.ITALIC, 25);
	static final Font BUTTON_FONT = new Font("Serif", Font.ITALIC, 20);
	static final Font ANSWER_FONT = new Font("Serif", Font.BOLD, 40);
	
	// the widgets shown on the answerpanel, other than the text. 
	JTextField textField = null;
	JButton checkAnswer = null; 
	JButton pass = null;
	JButton backButton = null;
	
	// info is just the information regarding the category and value.
	// you never know when the user will forget what the question belongs to.
	String info;
	
	// My dad advised me to do this instead of getting a parser class.
	// Obviously answers like "Who is Henry Ford" and "henry ford II?" are the same.
	// a whole list of stopwords, more clarification in the cleanString method.
	String[] stopWords = {"II", "III", "IV", "X", "Jr", "sir", "general", "colonel", "lieutenant", 
						"captain", "gen", "col", "lt", "capt", "mt", "miss", "mrs", "mr", "dr", 
						"mister", "the", "and", "or", "this", "that", "it", "is", "a", "an", "another", 
						"also", "as", "at", "for", "else", "if", "there", "here", "he", "she", "they", 
						"them", "her", "him", "why", "what", "who", "where", "when", "how", "because", 
						"since", "therefore", "however", "once", "thus", "who", "whom", "whomever", 
						"whoever", "were", "are", "was", "before", "after", "did", "do", "to", "what's",
						"who's", "where's", "how's", "when's", "why's", "there's", "that's", "of"};
	
	// initalize the board panel as an object.
	// this is to get access to the several setters and getters.
	JeopardyBoard board;
	
	// setter and getter for board
	public JeopardyBoard getBoard() {
		return board;
	}

	public void setBoard(JeopardyBoard board) {
		this.board = board;
	}

	// only pass the board in answer panel.
	public JeopardyAnswerPanel(JeopardyBoard board) {
		this.board = board;
	}
	
	// this puts and formats all the text and widgets onto the screen.
	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		
		// info shows the category and value of the question.
		info = "(CATEGORY: " + board.getCategory() + ",\nVALUE: " + board.getValue() + ")";
		
		g.setColor(Color.WHITE);
		g.setFont(QUESTION_FONT);
		
		// if this is the first time the program enters this code then proceed and initialize.
		// else modify.
		if(stopDuplicating == false) {
		  
		  // I don't want to write board.getBpx() and Bpy() all the time.
		  int x = board.getBpx(); 
		  int y = board.getBpy();
		  
		  // if user came to the question for the first time, widgets will be:
		  
		  /*
		   * 1. QUESTION in text
		   * 2. ENTRY in JTextField
		   * 3. ANSWER in JButton
		   * 4. PASS in JButton
		   * 5. INFO in text
		   */
		  
		  // else if user already answered and wants to see information, then widgets will be:
		  
		  /*
		   * 1. QUESTION in text
		   * 2. ANSWER in text
		   * 3. INFO in text
		   * 4. BACK in JButton
		   */
		  
		  if(board.userAttempted[x][y] == null) { 
			  textField = new JTextField();
			  textField.setBounds(150, 446, 500, 58); 
			  textField.setVisible(true);
			  textField.setFont(BUTTON_FONT); 
			  add(textField);
			  
			  checkAnswer = new JButton("Answer"); 
			  checkAnswer.setFont(BUTTON_FONT);
			  checkAnswer.setBounds(660, 450, 140, 50); 
			  checkAnswer.setBackground(Color.ORANGE);
			  checkAnswer.setOpaque(true);
			  checkAnswer.setBorderPainted(false);
			  checkAnswer.setVisible(true);
			  checkAnswer.addActionListener(this); 
			  add(checkAnswer);
			  
			  pass = new JButton("Pass"); 
			  pass.setFont(BUTTON_FONT);
			  
			  pass.setBounds(810, 450, 90, 50); 
			  pass.setBackground(Color.ORANGE);
			  pass.setOpaque(true);
			  pass.setBorderPainted(false);
			  pass.setVisible(true);
			  pass.addActionListener(this); 
			  add(pass);
			  
			  
			  // this formatting works, I don't know why the formatting to draw the category labels don't.
			  textFormat2.drawCenteredText(board.getQuestion().toUpperCase().substring(1,
					  board.getQuestion().length()-1), getFontMetrics(QUESTION_FONT), g, QUESTION_FONT, 100,
					  50, 950, 200);
			  
			  textFormat2.drawCenteredText(info, getFontMetrics(INFO_FONT), g, INFO_FONT,
					  100, 600, 950, 100); 
			  
			  
			  // once it performed the above actions, then it will longer have access to this part of the code.
			  stopDuplicating = true;
			  
		  } else {
			  			  
			  textFormat2.drawCenteredText(board.getQuestion().toUpperCase().substring(1,
					  board.getQuestion().length()-1), getFontMetrics(QUESTION_FONT), g, QUESTION_FONT, 100,
					  50, 950, 200);
					  
			  textFormat2.drawCenteredText("ANSWER:  " + board.getAnswer().toUpperCase(), getFontMetrics(ANSWER_FONT), g, ANSWER_FONT, 100, 425, 950, 165);
			  
			  
			  backButton = new JButton("Back"); 
			  backButton.setFont(BUTTON_FONT);
			  backButton.setBounds(420, 600, 210, 50); 
			  backButton.setBackground(Color.ORANGE);
			  backButton.setOpaque(true);
			  backButton.setBorderPainted(false);
			  backButton.setVisible(true);
			  backButton.addActionListener(this); 
			  add(backButton);
			  
			  // this code is actually sometimes useful. I don't know why, but without this, 
			  // there are still occurences when the actions are repeated more than once.
			  stopDuplicating = true;
		  }
		}
	}
	
	// simple method to print elements of array.
	public void printElements(String[] elements) {
		for(int x=0; x<elements.length; x++) {
			System.out.println(elements[x]);
		}
	}
	
	// Clean String method procedure:
		/* 
		 * 1. Pass the string and the list of stopwords (initialized above)
		 * 2. Make the string a list, check for stopwords in list of words and take them out.
		 * 3. Make the list of words a string and take out all punctuation.
		 */

	public String cleanString(String inputString, String[] stopwords) {
		
		
		String[] words = inputString.toLowerCase().split(" ");
		
		for(int x=0; x<stopwords.length; x++) {
			String stopword = stopwords[x];
			for(int y=0; y<words.length; y++) {
				if(words[y].equals(stopword)) {
					words[y] = "";
				}
			}
		}
		
		
		String finalString = "";
		
		for(int i=0; i<words.length; i++) {
			String word = words[i];
			finalString += word + " ";
		}
		
		finalString = finalString.replaceAll("\\W", "").toLowerCase().strip();
		
		
		return finalString.strip();
		
	}
	
	// Check if useranswer matches the actual answer.
	// Basically, check if answer is right or wrong.
	public void compare() {
		String useranswer = textField.getText();
		String answer = board.getAnswer();
		
		// delete text in textField because otherwise it will appear again.
		// just for the professionalism.
		textField.setText("");
		
		// 'clean' both strings, because when sorted the two may match.
		useranswer = cleanString(useranswer, stopWords);
		answer = cleanString(answer, stopWords);
		
		// if right, add points and set corresponding array position to true
		// if wrong, subtract points and set corresponding array position to false
		if(useranswer.equalsIgnoreCase(answer)) {
			board.addPoints();
			board.setUserAttempted(true);
		}else {		
			board.subtractPoints();
			board.setUserAttempted(false);
		}	
	}
	
	public void actionPerformed(ActionEvent e) {
		// if user pressed checkAnswer, then (only once) go to compare
		if(e.getSource() == checkAnswer) {
			board.getCl().show(board.getCards(), "Jeopardy! Board");
			compare();
			stopDuplicating = false;	// controls repetition in all cases
		} else if(e.getSource() == backButton || e.getSource() == pass) {
			board.getCl().show(board.getCards(), "Jeopardy! Board");
			back.setEnabled(true);
			stopDuplicating = false;
		} 
		// clean panel with built-in methods
		removeAll();
		repaint();
	}
	
	
}
