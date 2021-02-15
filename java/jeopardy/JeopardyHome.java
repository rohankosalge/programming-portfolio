package jeopardy;
/*
 * Programmer: Rohan Kosalge
 * 
 * Date: (First Day) March 25th, 2020
 * 		 (Last Update) May 1st, 2020
 * 
 * Purpose: Small home panel for the game. When you start the game, this is the first panel you see.
 * 			Tried to make it professional, with the introduction and image :)
 * 
 * 			Made sure I also added the "course info" (period, teacher).
 * 			After all, this is a school project.
 */

// import java.awt and java.event for listeners 
// import javax.swing for UI
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.print.DocFlavor.URL;
import javax.swing.*;

public class JeopardyHome extends JPanel implements ActionListener {
	
	// make an object out of my text formatting class.
	// really making use out of this class!
	TextFormat textFormat = new TextFormat();
	
	// cl and cards that gets the passed cl and cards values from the "parent" class.
	CardLayout cl;
	JPanel cards;
	
	// the first button you see when you start the program.
	JButton startGame;
	
	// pass cl and cards
	public JeopardyHome(CardLayout cl, JPanel cards) {
		this.cl = cl;
		this.cards = cards;
	}
	
	// constant fonts.
	static final Font AUTHOR_FONT = new Font("Impact", Font.BOLD, 20);
	static final Font BUTTON_FONT = new Font("Serif", Font.BOLD, 50);
	
	// button and decoration made here.
	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		
		// Set the color of the text
		g.setColor(Color.ORANGE);
		
		String author = "Rohan Kosalge presents...";
		String courseInfo = "Period 2 Java | Mr. Kulla";
		
		textFormat.drawCenteredLine(g, author, 130, 30, 790, 30, AUTHOR_FONT);
		g.drawString(courseInfo, 850, 690);
			
		System.out.println("class() ==" + getClass());
		java.net.URL url = getClass().getResource("../resources/jeopardy-logo.jpg");
		ImageIcon i = new ImageIcon(url);
		i.paintIcon(this, g, 130, 70);
		
		g.setColor(Color.BLACK);
		
		// making a background color properly visible is disgustingly long. 
		// you need .setOpaque and .setBorderPainted after .setBackground
		startGame = new JButton("Play Game!");
		startGame.setBackground(Color.ORANGE);
		startGame.setOpaque(true);
		startGame.setBorderPainted(false);
		startGame.setBounds(375, 550, 325, 70);
		startGame.setFont(BUTTON_FONT);
		startGame.addActionListener(this);
		
		// adds to the class, and recognized after the class is initialized as a JPanel 
		// in the parent class.
		add(startGame);
	}
	
	// only needed for the startGame button.
	public void actionPerformed(ActionEvent e) {		
		if(e.getSource() == startGame){
			cl.show(cards, "Jeopardy! Board");
		}
		// clean panel with built-in methods
		removeAll();
		repaint();		
	}
	
}
