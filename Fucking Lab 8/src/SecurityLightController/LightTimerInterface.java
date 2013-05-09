package SecurityLightController;

/**
 * This interface defines that which is used for a light timer.
 * 
 * @author schilling
 * 
 */
public interface LightTimerInterface {

	/**
	 * This method will start the timer.
	 * 
	 * @param delay
	 *            This is the delay, in seconds, for the given timer.
	 */
	public void startTimer(int delay);
}
