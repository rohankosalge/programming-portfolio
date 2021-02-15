package jeopardy;
/*
 * Programmer: Rohan Kosalge
 * 
 * Date: (First Day) March 25th, 2020
 * 		 (Last Update) May 1st, 2020
 * 
 * Purpose: Organize properties of each question into a class, called JQuestion.
 * 			Will have the simple properties - question, answer, category (cat), value (val)
 */
public class JQuestion {
	private String cat;
	private String question;
	private String answer;
	private int val;

	// when initialized, pass four strings (used in getQuestions when getting data)
	public JQuestion(String cat, String question, String answer, String val) {
		this.cat = cat;
		this.question = question;
		this.answer = answer;
		this.val = editVal(val);
		
		
	}
	
	// getters for each property, setters for value and question.
	// edit value - keep value type as Integer and not String. Take the dollar sign out.

	public String getCat() {
		return cat;
	}
	
	public String getQ() {
		return question;
	}
	
	public String getA() {
		return answer;
	}
	
	public int getVal() {
		return val;
	}
	
	public void setVal(int val) {
		this.val = val;
	}
	
	public void setQ(String question) {
		this.question = question;
	}
	
	public int editVal(String val) {
		int val2 = Integer.parseInt(val.replaceAll("[^0-9]", ""));
		return val2;
	}
	
	// print properties of the JQuestion out.
	public void print() {
		System.out.println(cat + ", " + question + ", " + answer + ", " + val);
	}
}
