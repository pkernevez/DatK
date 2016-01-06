package dojo;

public class UnitsCouple {

	public UnitsCouple(String unit, String bigUnit) {
		super();
		this.unit = unit;
		this.bigUnit = bigUnit;
	}

	private String unit;
	private String bigUnit;

	public String getUnit() {
		return unit;
	}

	public void setUnit(String unit) {
		this.unit = unit;
	}

	public String getBigUnit() {
		return bigUnit;
	}

	public void setBigUnit(String bigUnit) {
		this.bigUnit = bigUnit;
	}

}
