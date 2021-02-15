package jeopardy;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Random;

public class SortQuestions {
	
	private int catNum;
	
	public SortQuestions() {
		
	}
	
	public int getCatNum(JQuestion[][] jqs) {
		for(int i=0; i<jqs.length; i++) {
			for(int j=0; j<jqs[i].length; j++) {
				if(jqs[i][j] == null) {
					catNum++;
				}
			}
		}
		return catNum;
	}
	
	public JQuestion[][] sort() {
		
		GetQuestions launcher = new GetQuestions();
		JQuestion[] questions = launcher.get();
		
		JQuestion[][] sortedQs = new JQuestion[84][5];
		
		for(int x=0; x<420; x++) {
			JQuestion jq = questions[x];
			removeExtras(jq);
			String cat = jq.getCat();
			
			outerloop:
			for (int i=0; i<84; i++) {
				for (int j=0; j<5; j++) {
					if(sortedQs[i][j] == null) {
						if(j==0) {
							sortedQs[i][j] = jq;
							break outerloop;
						}
						else if(j!=0) {
							JQuestion sjq = sortedQs[i][0];
							String gcat = sjq.getCat();
							if(gcat.equals(cat)) {
								sortedQs[i][j] = jq;
								break outerloop;
							}
						}
					}
				}
			}
		}
		
		for(int i=0; i<sortedQs.length; i++) {
			for(int j=0; j<sortedQs[i].length; j++) {
				JQuestion jq = sortedQs[i][j];
				String qq = jq.getQ();
				
				jq.setVal((j+1)*200);
				
				if(qq.contains(".jpg") == true) {
					Arrays.fill(sortedQs[i], null);
					break;
				}
			}
		}
		
		
		int lim = getCatNum(sortedQs);
		
		JQuestion[][] newQList = new JQuestion[84-lim][5];
		
		int counter=0;
		
		outerloop:
		for(int i=0; i<sortedQs.length; i++) {
			if(sortedQs[i][0] != null) {
				for(int j=0; j<5; j++) {					
					newQList[counter][j] = sortedQs[i][j];
				}
				counter++;
				
				if(counter==lim) {
					break outerloop;
				}
			}
		}
		return newQList;
	}
	
	// removeExtras will remove extra links
	// loop through characters in jq.question
	// and check for < and >, then replace everything
	// in between with ""
	public void removeExtras(JQuestion jq) {
		String question = jq.getQ();
		
		int beginIndex=0; int endIndex; int finalX=0;
		
		outerloop:
		while(finalX!=question.length()-1) {
			finalX=0;
			for(int x=0; x<question.length(); x++){
				if(question.charAt(x) == '<') {
					beginIndex = x;
				}
				if(question.charAt(x) == '>') {
					endIndex = x;
					
					String removeStr = question.substring(beginIndex, endIndex+1);
					question = question.replace(removeStr, "");
					break;
							
				}
				finalX++;
				if(finalX==question.length()-1) {
					break outerloop;
				}
			}
		}
		
		
		jq.setQ(question);
	}
	
	public void printQs(JQuestion[][] jqs) {
		for(int x=0; x<jqs.length; x++) {
			for(int y=0; y<jqs[x].length; y++) {
				if(jqs[x][y]!=null) {
					jqs[x][y].print();
				}else {
					System.out.println("null");
				}
			}
		}
	}
	
	public int getCatNum() {
		return catNum;
	}
	
	public JQuestion[][] randsort() {
		JQuestion[][] qList = sort();
		JQuestion[][] userQs = new JQuestion[7][5];
		
		ArrayList<Integer> list = new ArrayList<Integer>();
	    for (int i=0; i<50; i++) {
	        list.add(i);
	    }
	    
	    Collections.shuffle(list);
	    for (int i=0; i<7; i++) {
	        userQs[i] = qList[list.get(i)];
	    }

	    return userQs;
	}
}
