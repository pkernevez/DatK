package dojo;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

import exception.InvalidCardException;

public class CardTest {

	@Test
	public void testGetLevelForA2() throws Exception {
		Card tCard = new Card("2-H");
		assertEquals("2", tCard.getLevel());
	}

	@Test
	public void testGetLevelForA10() throws Exception {
		Card tCard = new Card("10-C");
		assertEquals("10", tCard.getLevel());
	}

	@Test
	public void testGetColor() throws Exception {
		Card tCard = new Card("2-C");
		assertEquals("C", tCard.getColor());
	}

	@Test
	public void testCompare2lessQ() throws Exception {
		Card tCard2 = new Card("2-C");
		Card tCardQ = new Card("Q-C");
		assertEquals(-10, tCard2.compareTo(tCardQ));
	}

	@Test
	public void testCompare10Eq10() throws Exception {
		Card tCard1 = new Card("10-D");
		Card tCard2 = new Card("10-H");
		assertEquals(0, tCard1.compareTo(tCard2));
	}

	@Test(expected = InvalidCardException.class)
	public void testCardInvalidity() throws Exception {
		new Card("10-Y");
	}

	@Test
	public void testGetStrengthForNumeric() throws Exception {
		assertEquals(2, new Card("2-H").getStrength());
	}

	@Test
	public void testGetStrengthForQueen() throws Exception {
		assertEquals(12, new Card("Q-H").getStrength());
	}

	@Test
	public void testEqualYes() throws InvalidCardException {
		assertEquals(new Card("4-D"), new Card("4-D"));
	}

}
