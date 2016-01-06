package dojo;

public class Roman {

	public String convertLessThanTen(int number) {
		return convert(number, 1, "I", "V", "X");
	}

	public String convert(int number) {
		String res = "";
		if (number / 10 > 0) {
			res = convert((number / 10) * 10, 10, "X", "L", "C");
		}
		if (number % 10 > 0) {
			res += convert(number % 10, 1, "I", "V", "X");
		}
		return res;
	}

	public String convert(int number, int unit, String symbol, String fiveTimeSymbol, String nextSymbol) {
		String romanNumeral = "";
		if (number < 4 * unit) {
			romanNumeral = repeat(symbol, number);
		} else if (number == 4 * unit) {
			romanNumeral = symbol + fiveTimeSymbol;
		} else if (number == 5 * unit) {
			romanNumeral = fiveTimeSymbol;
		} else if (number < 9 * unit) {
			romanNumeral = fiveTimeSymbol + convert(number - 5 * unit, unit, symbol, fiveTimeSymbol, nextSymbol);
		} else if (number == 9 * unit) {
			romanNumeral = symbol + nextSymbol;
		}
		return romanNumeral;
	}

	public String repeat(String c, int i) {
		StringBuffer res = new StringBuffer();
		for (int j = 0; j < i; j++) {
			res.append(c);
		}
		return res.toString();
	}

	public String convertGreaterThan9(int number) {
		String romanNumeral = "";
		if (number == 10) {
			romanNumeral = "X";
		} else if (number < 20) {
			romanNumeral = "X" + convertLessThanTen(number - 10);
		} else if (number < 30) {
			romanNumeral = "XX" + convertLessThanTen(number - 20);
		}
		return romanNumeral;
	}

}
