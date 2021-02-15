package jeopardy;
/*
 * Programmer: Rohan Kosalge
 * 
 * Date: (First Day) March 25th, 2020
 * 		 (Last Update) May 1st, 2020
 * 
 * Purpose: To get list of questions from a JSON file. 
 * 			I looked online and found a JSON file of the entire Jeopardy! database.
 * 			My dad and I were able to shorten it and get the data that I wanted, thanks to some terminal work.
 * 			
 * 			Then I made the JQuestion class and wrote this class.
 * 			It only contains one function called get(), that returns a sorted list of questions (by category).
 */

// import these to catch exceptions and to read the file.
import java.io.FileNotFoundException;
import java.io.FileReader;

// import these solely for file reading, managing, and parsing. 
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class GetQuestions {
	public GetQuestions() {
		
	}
	public JQuestion[] get() {
		
		// create parser object and empty list to hold the questions.
		JSONParser parser = new JSONParser();
		JQuestion[] qList = new JQuestion[420];
		
		// read the file I have, sort it out.
		// JSON files are easy to read because of its simple organization.
		try (FileReader reader = new FileReader("/Users/rohankosalge/Downloads/jQuestionsShortFinalizedV3")){
			JSONArray jarray = (JSONArray) parser.parse(reader);
			
		     // iterating ArrayList
			 int x = 0;
		     for(Object obj:jarray) {
		    	 
		    	// get the four values: question, answer, category, and value.
		    	// only include recent questions (sort by air date) and rounds labelled "Jeopardy!"
		    	JSONObject jobj = (JSONObject)obj;		    	
		    	String question = (String) jobj.get("question");
		    	String answer = (String) jobj.get("answer");
		    	String cat = (String) jobj.get("category");
		    	String val = ((String) jobj.get("value"));
		    	
		    	String roundType = ((String) jobj.get("round"));
		    	String airDate = ((String) jobj.get("air_date"));
		    	
		    	//System.out.println(airDate);
		    	int newAirDate = Integer.parseInt(airDate.substring(0, 4));
		    	
		    	if(roundType.equals("Jeopardy!") && newAirDate>2001) {
		    		JQuestion q = new JQuestion(cat, question, answer, val);	
		    		
		    		// add question to master list.
			        qList[x] = q;
			        x++;
		    	}
		        
		     }
			
		// for catching.
		} catch (FileNotFoundException fe) {
			fe.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		// return the whole master list of questions. 
		return qList;
	}
}
