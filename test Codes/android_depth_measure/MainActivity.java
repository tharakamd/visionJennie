package com.example.dilan.btmsn;

import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.util.Log;
import android.view.MenuItem;
import android.view.SurfaceView;

import org.opencv.android.JavaCameraView;
import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.CameraBridgeViewBase.CvCameraViewFrame;
import org.opencv.android.CameraBridgeViewBase.CvCameraViewListener2;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.calib3d.StereoBM;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.DMatch;
import org.opencv.core.KeyPoint;
import org.opencv.core.Mat;
import org.opencv.core.MatOfDMatch;
import org.opencv.core.MatOfKeyPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.features2d.DescriptorExtractor;
import org.opencv.features2d.DescriptorMatcher;
import org.opencv.features2d.FeatureDetector;
import org.opencv.features2d.Features2d;
import org.opencv.imgproc.Imgproc;

import java.util.LinkedList;
import java.util.List;

public class MainActivity extends AppCompatActivity implements CvCameraViewListener2 {

    public final static String EXTRA_MESSAGE = "com.example.dilan.btmsn.MESSAGE";
    // Used for logging success or failure messages
    private static final String TAG = "OCVSample::Activity";

    // Loads camera view of OpenCV for us to use. This lets us see using OpenCV
    private CameraBridgeViewBase mOpenCvCameraView;

    // Used in Camera selection from menu (when implemented)
    private boolean mIsJavaCamera = true;
    private MenuItem mItemSwitchCamera = null;

    // These variables are used (at the moment) to fix camera orientation from 270degree to 0degree
    Mat mRgba;
    Mat mRgbaF;
    Mat mRgbaT;

    // variables to the depth map
    private static Mat frame_previous;
    private static Mat frame_previous_out;
    private static int frame_number;
    Mat frame_first;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.show_camera);
        mOpenCvCameraView = (JavaCameraView) findViewById(R.id.show_camera_activity_java_surface_view);
        mOpenCvCameraView.setVisibility(SurfaceView.VISIBLE);
        mOpenCvCameraView.setCvCameraViewListener(this);
        frame_number = -2;
    }


    private BaseLoaderCallback mLoaderCallback = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {
            switch (status) {
                case LoaderCallbackInterface.SUCCESS: {
                    Log.i(TAG, "OpenCV loaded successfully");
                    mOpenCvCameraView.enableView();
                }
                break;
                default: {
                    super.onManagerConnected(status);
                }
                break;
            }
        }
    };

    @Override
    public void onPause() {
        super.onPause();
        if (mOpenCvCameraView != null)
            mOpenCvCameraView.disableView();
    }

    @Override
    public void onResume() {
        super.onResume();
        if (!OpenCVLoader.initDebug()) {
            Log.d(TAG, "Internal OpenCV library not found. Using OpenCV Manager for initialization");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_0_0, this, mLoaderCallback);
        } else {
            Log.d(TAG, "OpenCV library found inside package. Using it!");
            mLoaderCallback.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        }
    }

    public void onDestroy() {
        super.onDestroy();
        if (mOpenCvCameraView != null)
            mOpenCvCameraView.disableView();
    }

    @Override
    public void onCameraViewStarted(int width, int height) {
        mRgba = new Mat(height, width, CvType.CV_8UC4);
        mRgbaF = new Mat(height, width, CvType.CV_8UC4);
        mRgbaT = new Mat(width, width, CvType.CV_8UC4);
    }

    @Override
    public void onCameraViewStopped() {
        mRgba.release();
    }

    @Override
    public Mat onCameraFrame(CvCameraViewFrame inputFrame) {
        Mat frame_final;
        if (frame_number < 0) {
            frame_first = inputFrame.gray();
            Core.flip(frame_first, frame_first, 1);
            Core.flip(frame_first, frame_first, 0);
            frame_previous = frame_first.clone();
            frame_previous_out = frame_first.clone();
        }
        if (frame_number >= 50) {
            frame_number = 0;
            Mat frame_this = inputFrame.gray();
            Core.flip(frame_this, frame_this, 1);
            Core.flip(frame_this, frame_this, 0);
/////////////////////////////////////////////////////////

            Mat refMat = frame_this.clone();
            Mat srcMat = frame_previous.clone();

            MatOfDMatch matches = new MatOfDMatch();
            MatOfDMatch goodMatches = new MatOfDMatch();

            LinkedList<DMatch> listOfGoodMatches = new LinkedList<>();

            LinkedList<Point> refObjectList = new LinkedList<>();
            LinkedList<Point> srcObjectList = new LinkedList<>();

            MatOfKeyPoint refKeypoints = new MatOfKeyPoint();
            MatOfKeyPoint srcKeyPoints = new MatOfKeyPoint();

            Mat refDescriptors = new Mat();
            Mat srcDescriptors = new Mat();

            MatOfPoint2f reference = new MatOfPoint2f();
            MatOfPoint2f source = new MatOfPoint2f();

            FeatureDetector orbFeatureDetector = FeatureDetector.create(FeatureDetector.ORB);
            orbFeatureDetector.detect(refMat, refKeypoints);
            orbFeatureDetector.detect(srcMat, srcKeyPoints);

            DescriptorExtractor descriptorExtractor = DescriptorExtractor.create(DescriptorExtractor.ORB);
            descriptorExtractor.compute(refMat, refKeypoints, refDescriptors);
            descriptorExtractor.compute(srcMat, srcKeyPoints, srcDescriptors);

            DescriptorMatcher matcher = DescriptorMatcher.create(DescriptorMatcher.BRUTEFORCE_HAMMING);
            matcher.match(refDescriptors, srcDescriptors, matches);

            double max_dist = 0;
            double min_dist = 100;
            List<DMatch> matchesList = matches.toList();

            for (int i = 0; i < refDescriptors.rows(); i++) {
                Double distance = (double) matchesList.get(i).distance;
                if (distance < min_dist) min_dist = distance;
                if (distance > max_dist) max_dist = distance;
            }

            for (int i = 0; i < refDescriptors.rows(); i++) {
                if (matchesList.get(i).distance < 30 * min_dist) {
                    listOfGoodMatches.add(matchesList.get(i));
                }
            }

            goodMatches.fromList(listOfGoodMatches);

            List<KeyPoint> refObjectListKeypoints = refKeypoints.toList();
            List<KeyPoint> srcObjectListKeypoints = srcKeyPoints.toList();

            for (int i = 0; i < listOfGoodMatches.size(); i++) {
                refObjectList.addLast(refObjectListKeypoints.get(listOfGoodMatches.get(i).queryIdx).pt);
                srcObjectList.addLast(srcObjectListKeypoints.get(listOfGoodMatches.get(i).trainIdx).pt);
            }

            reference.fromList(refObjectList);
            source.fromList(srcObjectList);
            Mat outputImage = new Mat();
            Features2d.drawMatches(refMat, refKeypoints, srcMat, srcKeyPoints, goodMatches, outputImage);

            System.out.println(frame_this.size() + "  " + outputImage.size());
            outputImage.convertTo(outputImage,0);
            Imgproc.resize(outputImage,outputImage,frame_this.size());
///////////////////////////////////////////////////////////
            frame_previous = frame_this.clone();
            frame_previous_out = outputImage.clone();
            frame_final = outputImage.clone();
        } else {
            frame_final = frame_previous_out.clone();
        }
        frame_number++;
        return frame_final; // This function must return
    }
}
