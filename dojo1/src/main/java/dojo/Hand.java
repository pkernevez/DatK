package dojo;

import java.util.HashSet;
import java.util.Set;

public class Hand {

	public Set<Card> cards;
	public Hand(String s) {
		cards = new HashSet<Card>();
		for(String t:s.split(" ")){
			cards.add(new Card(t));
		}
	}
	public boolean contains(Card card) {
		return cards.contains(card);
	}
	
}
