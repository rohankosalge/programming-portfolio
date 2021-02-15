package jeopardy;
/*
 * Programmer: Rohan Kosalge
 * 
 * Date: (First Day) March 25th, 2020
 *       (Last Update) May 1st, 2020
 * 
 * Purpose: The whole Jeopardy! game! Or, most of it. In the proposal I was
 * 			really putting in ideas as if they were easy to code. I really thought too far about the project.
 * 			
 * 			As of May 1st, 2020, this game can properly do a regular Jeopardy! round, with points and friendly UI.
 * 
 * 			I'm not really thinking of doing a Double Jeopardy! or even Final Jeopardy!, even though I know they will
 * 			be much easier to code. It's just that the smallest changes can start big problems and can totally ruin my code,
 * 			even with access to revision history and undoing. I could make a copy project, but things may get confusing.
 * 
 * 			Plus, this game is quite sleek! It uses actual data from real Jeopardy! games in the last few decades. 
 * 			So I'm quite proud of what I've done. 
 */

// import java.awt and java.event for listeners 
// import javax.swing for UI
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class Jeopardy3 extends JPanel implements ActionListener, MouseListener{
	
	// total number of points. Literally the most important variable, game-wise.
	public static int points = 0;
		
	// keep all fonts constant, starting with J_FONT.
	static final Font J_FONT = new Font("Impact", Font.BOLD, 40);
		
	// declare object of SortQuestions to randomly sort questions (by category) in finalizedUserQuestions
	// that method is called randsort, seen in setupWindow. The question in finalizedUserQuestions are the ones
	// shown on the board.
	SortQuestions sortQuestions = new SortQuestions();
	JQuestion[][] finalizedUserQuestions;
	
	// cl and cards are passed through every panel. 
	// cl is the layout manager, and cards is the parent panel.
	// easy to understand that this game's layout is CardLayout.
	public CardLayout cl; 
	JPanel cards; 
	
	public static JMenuItem back;
	
	public JMenuItem getBack() {
		return back;
	}
	
	// these getters are for the other panels, not this one.
	public CardLayout getCl() {
		return cl;
	}

	public JPanel getCards() {
		return cards;
	}

	
	// the first button you see when you start the program.
	// this is actually used in the home panel, but is here because it
	// has to be recognized in actionPerformed.
	JButton startGame;
	// the JFrame
	public JFrame f;
	
	// without mouseListener you won't be able to click on the questions and answer.
	// since everything is controlled here, you need to use mouselistener here even though
	// it technically isn't used here.
	public Jeopardy3() {
		addMouseListener(this);
	}
		
	// the panels, menu, and other important fields are made here.
	public void setupWindow() {
		// all the variables declared above are initialized here.
		finalizedUserQuestions = sortQuestions.randsort();
		cards = new JPanel(new CardLayout());		
		cl = (CardLayout)(cards.getLayout());
			
		f = new JFrame("Jeopardy!");
		f.setResizable(false);
		JPanel home = new JeopardyHome(cl, cards);
		home.setBackground(Color.BLUE);
		JPanel board = new JeopardyBoard(cl, cards, finalizedUserQuestions);
		JPanel answerpanel = new JeopardyAnswerPanel((JeopardyBoard) board);
		answerpanel.setBackground(Color.BLUE);
		JPanel endpanel = new JeopardyGameEnd();
		endpanel.setBackground(Color.BLUE);
		
		cards.add(home, "Main");
		cards.add(board, "Jeopardy! Board");
		cards.add(answerpanel, "Jeopardy! Answer");
		cards.add(endpanel, "End");
		
		cl.show(cards, "Main");
		
		// menu widgets. This game isn't really that menu-oriented.
		// 'Exit' and 'Back to Home' are the only features.
		
		JMenuBar menuBar = new JMenuBar();
		JMenu options = new JMenu("Options");
		JMenuItem exit = new JMenuItem("Exit");
		back = new JMenuItem("Go To Board");
		
		exit.addActionListener(this);
		back.addActionListener(this);
		
		options.add(back);
		options.add(exit);
		menuBar.add(options);
		
		// frame "control center"
		f.setJMenuBar(menuBar);	
		f.setSize(1050, 745);
		f.setLocationRelativeTo(null);
		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		f.add(cards, BorderLayout.CENTER);
				
		f.setVisible(true);
	}
	
	// run setupWindow, watch the magic happen.
	public static void main(String[] args){		
		Jeopardy3 j = new Jeopardy3();
		j.setupWindow();
	}

	// change panels here
	public void actionPerformed(ActionEvent e) {	
		// built-in methods used to clear any unneeded widgets, 
		// bring new widgets and repaint. Otherwise the previous widgets
		// will still be there.
		removeAll();
		repaint();
				
		if(e.getSource() == startGame){
			cl.show(cards, "Jeopardy! Board");
		}
		
		if(e.getActionCommand() == "Exit") { 
			cl.show(cards, "End");
			back.setEnabled(true);
		}else if(e.getActionCommand() == "Go To Board") {
			cl.show(cards, "Jeopardy! Board");  
		}
		
		
		
	}

	// you will get an error without these useless methods...
	
	public void mouseClicked(MouseEvent e) {
	}
	public void mousePressed(MouseEvent e) {
	}
	public void mouseReleased(MouseEvent e) {
	}
	public void mouseEntered(MouseEvent e) {		
	}
	public void mouseExited(MouseEvent e) {
	}
}