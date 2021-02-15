package jeopardy;
/*
 * Programmer: Rohan Kosalge
 * 
 * Date: (First Day) May 14th, 2020
 * 		 (Last Update) May 14th, 2020
 * 
 * Purpose: The ending panel for the game, just to make the project more complete.
 * 			I decided that there is no winning or losing (no point goal). 
 * 			Whenever the user decides to quit or if they attempted all questions, 
 * 			they will be taken to this panel, with the total number of points shown.
 * 			
 * 			Pretty simple. I will try to make this panel look nice as well. 
 * 			Make it look professional. 	
 */

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class JeopardyGameEnd extends JPanel implements ActionListener {
	
	TextFormat textFormat = new TextFormat();
	
	static final Font SUB_FONT = new Font("Impact", Font.BOLD, 20);
	static final Font POINTS_FONT = new Font("Serif", Font.BOLD, 50);
	static final Font BUTTON_FONT = new Font("Serif", Font.BOLD, 30);
	
	JButton exit;
	
	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		
		removeAll();
		String intro = "Thank you for playing...";
		String pointsText = "TOTAL POINTS: " + Jeopardy3.points;
		String creatorText = "Made by: Rohan Kosalge";
		String courseInfo = "Period 2 Java | Mr. Kulla";
		
		g.setColor(Color.ORANGE);	
		textFormat.drawCenteredLine(g, intro, 130, 30, 790, 30, SUB_FONT);
		
		ImageIcon i = new ImageIcon("/Users/rohankosalge/Downloads/jeopardy-logo.jpg");
		i.paintIcon(this, g, 130, 70);
		
		g.setColor(Color.WHITE);
		textFormat.drawCenteredLine(g, pointsText, 130, 470, 790, 200, POINTS_FONT);
		
		g.setColor(Color.ORANGE);
		g.setFont(SUB_FONT);
		g.drawString(creatorText, 15, 690);
		g.drawString(courseInfo, 850, 690);
		
		g.setColor(Color.BLACK);
		
		
		exit = new JButton("EXIT");
		exit.setBackground(Color.ORANGE);
		exit.setOpaque(true);
		exit.setBorderPainted(false);
		exit.setBounds(475, 630, 125, 45);
		exit.setFont(BUTTON_FONT);
		exit.addActionListener(this);
		
		add(exit);
	}
	
	public void actionPerformed(ActionEvent e) {
		removeAll();
		repaint();		
		if(e.getSource() == exit) {
			System.exit(0);
		}
	}
}
