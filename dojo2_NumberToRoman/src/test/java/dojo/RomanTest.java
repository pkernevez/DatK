package dojo;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class RomanTest {

	private Roman roman = new Roman();

	@Test
	public void testConvertLessThanTen1InRoman() throws Exception {
		assertEquals("I", roman.convertLessThanTen(1));
	}

	@Test
	public void testConvertLessThanTen2inRoman() throws Exception {
		assertEquals("II", roman.convertLessThanTen(2));
	}

	@Test
	public void testConvertLessThanTen3InRoman() throws Exception {
		assertEquals("III", roman.convertLessThanTen(3));
	}

	@Test
	public void testConvertLessThanTen4InRoman() throws Exception {
		assertEquals("IV", roman.convertLessThanTen(4));
	}

	@Test
	public void testConvertLessThanTen5InRoman() throws Exception {
		assertEquals("V", roman.convertLessThanTen(5));
	}

	@Test
	public void testConvertLessThanTen6InRoman() throws Exception {
		assertEquals("VI", roman.convertLessThanTen(6));
	}

	@Test
	public void testConvertLessThanTen9InRoman() throws Exception {
		assertEquals("IX", roman.convertLessThanTen(9));
	}

	@Test
	public void testConvert10InRoman() throws Exception {
		assertEquals("X", roman.convertGreaterThan9(10));
	}

	@Test
	public void testConvert11InRoman() throws Exception {
		assertEquals("XI", roman.convertGreaterThan9(11));
	}

	@Test
	public void testRepeat() throws Exception {
		assertEquals("II", roman.repeat("I", 2));
	}

	@Test
	public void testConvert99InRoman() throws Exception {
		assertEquals("XCIX", roman.convert(99));
	}

}
