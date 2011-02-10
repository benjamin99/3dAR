package test.ThreeDAR.beta;

import android.app.Activity;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.view.Window;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.widget.TextView;

public class ThreeDARMainActivity extends Activity implements SensorEventListener{
	
	private PreviewView 	_previewView;
	private TextView		_sensorTextView;
	private SensorManager 	_sensorManager;
	
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        //Set the activity to be NO_TITLE and NO_STATUS_BAR:
        final Window win = getWindow();
        win.setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        requestWindowFeature(Window.FEATURE_NO_TITLE);

        setContentView(R.layout.main);
        _previewView = (PreviewView) findViewById(R.id.preview_view);
        _sensorTextView = (TextView) findViewById(R.id.sensor_text_view);
        
        //Get the sensor manager from the system:
        _sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);

    }
    
    @Override
    public void onResume() {
    	
    	super.onResume();
    	
    	//Register the sensor listener:
        _sensorManager.registerListener(this,
    			_sensorManager.getDefaultSensor(Sensor.TYPE_ORIENTATION),
    			_sensorManager.SENSOR_DELAY_GAME);
    }

    @Override
    public void onStop() {
    	//Unregister the sensor listener:
    	_sensorManager.unregisterListener(this);
    	super.onStop();
    }

	@Override
	public void onAccuracyChanged(Sensor arg0, int arg1) {
		//Should not have to implement this function	
	}


	@Override
	public void onSensorChanged(SensorEvent event) {
		//Will be called when sensing new data values
		if(event.sensor.getType() == Sensor.TYPE_ORIENTATION ) {
			//Only receiving the orientation data so far:
			String textStr = "Orrientation: x:"
				             + Float.toString(event.values[0])
				             + " y:" + Float.toString(event.values[1])
				             + " z:" + Float.toString(event.values[2]);
			_sensorTextView.setText(textStr);
			
		}
		
	}
}