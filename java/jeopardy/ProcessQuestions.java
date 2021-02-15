package jeopardy;

public class ProcessQuestions {
	private JQuestion[][] qList;
	public ProcessQuestions() {
		SortQuestions sortQuestions = new SortQuestions();	
		JQuestion[][] qList = sortQuestions.sort();
	}
	
	public JQuestion[][] getQList(){
		return qList;
	}
	
}
