package dojo;

import java.util.HashSet;
import java.util.Set;

import com.google.common.collect.Ordering;

public class Hand implements Comparable<Hand> {

	public Set<Card> cards;

	public Hand(String s) {
		cards = new HashSet<Card>();
		for (String t : s.split(" ")) {
			cards.add(new Card(t));
		}
	}

	public boolean contains(Card card) {
		return cards.contains(card);
	}

	@Override
	public int compareTo(Hand h) {
		return this.strongerCard().compareTo(h.strongerCard());
	}

	public Card strongerCard() {
		return Ordering.natural().max(cards);
	}

}
