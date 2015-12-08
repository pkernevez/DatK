package dojo;

public class Card implements Comparable<Card> {

	private String level;
	private String color;
	
	public Card(String string) {
		level =  string.split("-")[0];
		color = string.split("-")[1];
	}

	public String getLevel(){
		return level;
	}
	
	
	
	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((color == null) ? 0 : color.hashCode());
		result = prime * result + ((level == null) ? 0 : level.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Card other = (Card) obj;
		if (color == null) {
			if (other.color != null)
				return false;
		} else if (!color.equals(other.color))
			return false;
		if (level == null) {
			if (other.level != null)
				return false;
		} else if (!level.equals(other.level))
			return false;
		return true;
	}

	public int getStrength(){
		int result;
		switch (level) {
		case "A":
			result = 14;
			break;
		case "K":
			result = 13;
			break;
		case "Q":
			result = 12;
			break;
		case "J":
			result = 11;
			break;
		default:
			result = Integer.parseInt(level);
		}
		return result;
	}
	
	public String getColor(){
		return color;
	}

	public int compareTo(Card o) {
//		if(o.level.equals(level))
//			return 0;
//		else if(o.level.equals(level))
//		; 
		return 0;
	}
	
}
