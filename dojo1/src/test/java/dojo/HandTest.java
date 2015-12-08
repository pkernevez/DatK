package dojo;

import static org.junit.Assert.assertTrue;

import org.junit.Test;


public class HandTest {

	@Test
	public void testHandString() throws Exception {
		Hand h=new Hand("2-D 3-D 4-D 5-D 6-D");
		assertTrue(h.contains(new Card("4-D")));
	}

}
