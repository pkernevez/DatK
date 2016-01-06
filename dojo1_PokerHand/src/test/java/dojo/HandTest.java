package dojo;

import static org.junit.Assert.assertTrue;

import org.junit.Test;

public class HandTest {

	@Test
	public void testHandString() throws Exception {
		Hand h = new Hand("2-D 3-D 4-D 5-D 6-D");
		assertTrue(h.contains(new Card("4-D")));
	}

	@Test
	public void testHigherCardInHandWithNoCombi() throws Exception {
		Hand h = new Hand("2-C 3-H K-D 7-D 9-C");
		Hand h2 = new Hand("2-H 6-C Q-S 4-C 9-H");

		assertTrue("Invalid hand expected 0: returns " + h.compareTo(h2), h.compareTo(h2) > 0);
	}

}
