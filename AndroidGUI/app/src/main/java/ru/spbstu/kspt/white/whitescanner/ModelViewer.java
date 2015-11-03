package ru.spbstu.kspt.white.whitescanner;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.lang.reflect.Field;

import javax.microedition.khronos.egl.EGL10;
import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.egl.EGLDisplay;
import javax.microedition.khronos.opengles.GL10;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.res.AssetManager;
import android.content.res.Resources;
import android.graphics.drawable.Drawable;
import android.opengl.GLSurfaceView;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.MotionEvent;
import android.view.View;

import com.threed.jpct.Camera;
import com.threed.jpct.FrameBuffer;
import com.threed.jpct.Light;
import com.threed.jpct.Logger;
import com.threed.jpct.Loader;
import com.threed.jpct.Matrix;
import com.threed.jpct.Object3D;
import com.threed.jpct.Primitives;
import com.threed.jpct.RGBColor;
import com.threed.jpct.SimpleVector;
import com.threed.jpct.Texture;
import com.threed.jpct.TextureManager;
import com.threed.jpct.World;
import com.threed.jpct.util.BitmapHelper;
import com.threed.jpct.util.MemoryHelper;

/**
 * Created by Borisov Victor.
 */
public class ModelViewer extends AppCompatActivity /*Activity*/ {

    // Used to handle pause and resume...
    private static ModelViewer master = null;

    private GLSurfaceView mGLView;
    private MyRenderer renderer = null;
    private FrameBuffer fb = null;
    private World world = null;
    private RGBColor back = new RGBColor(50, 50, 100);

    private float touchTurn = 0;
    private float touchTurnUp = 0;

    private float xpos = -1;
    private float ypos = -1;

    private Object3D m_model = null;
    private int fps = 0;
    private boolean gl2 = true;

    private Light sun = null;

    private boolean isForceRefresh = false;

    private String m_modelName = "";
    private int m_modelScale = 1;

    protected void onCreate(Bundle savedInstanceState) {

        Logger.log("onCreate");

        if (master != null) {
            copy(master);
        }

        Intent intent = getIntent();
        m_modelName = intent.getStringExtra(ModelsList.EXTRA_MESSAGE);
        isForceRefresh = true;

        setTitle(m_modelName);

        super.onCreate(savedInstanceState);

        mGLView = new GLSurfaceView(getApplication());

        if (gl2) {
            mGLView.setEGLContextClientVersion(2);
        } else {
            mGLView.setEGLConfigChooser(new GLSurfaceView.EGLConfigChooser() {
                public EGLConfig chooseConfig(EGL10 egl, EGLDisplay display) {
                    // Ensure that we get a 16bit framebuffer. Otherwise, we'll
                    // fall back to Pixelflinger on some device (read: Samsung
                    // I7500). Current devices usually don't need this, but it
                    // doesn't hurt either.
                    int[] attributes = new int[] { EGL10.EGL_DEPTH_SIZE, 16, EGL10.EGL_NONE };
                    EGLConfig[] configs = new EGLConfig[1];
                    int[] result = new int[1];
                    egl.eglChooseConfig(display, attributes, configs, 1, result);
                    return configs[0];
                }
            });

        }

        renderer = new MyRenderer();
        mGLView.setRenderer(renderer);
        setContentView(mGLView);
    }

    @Override
    protected void onPause() {
        super.onPause();
        mGLView.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        mGLView.onResume();
    }

    @Override
    protected void onStop() {
        super.onStop();
    }

    private void copy(Object src) {
        try {
            Logger.log("Copying data from master Activity!");
            Field[] fs = src.getClass().getDeclaredFields();
            for (Field f : fs) {
                f.setAccessible(true);
                f.set(this, f.get(src));
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public boolean onTouchEvent(MotionEvent me) {

        if (me.getAction() == MotionEvent.ACTION_DOWN) {
            xpos = me.getX();
            ypos = me.getY();
            return true;
        }

        if (me.getAction() == MotionEvent.ACTION_UP) {
            xpos = -1;
            ypos = -1;
            touchTurn = 0;
            touchTurnUp = 0;
            return true;
        }

        if (me.getAction() == MotionEvent.ACTION_MOVE) {
            float xd = me.getX() - xpos;
            float yd = me.getY() - ypos;

            xpos = me.getX();
            ypos = me.getY();

            touchTurn = xd / -100f;
            touchTurnUp = yd / -100f;
            return true;
        }

        try {
            Thread.sleep(15);
        } catch (Exception e) {
            // No need for this...
        }

        return super.onTouchEvent(me);
    }

    protected boolean isFullscreenOpaque() {
        return true;
    }

    class MyRenderer implements GLSurfaceView.Renderer {

        private long time = System.currentTimeMillis();

        public MyRenderer() {
        }

        public void onSurfaceChanged(GL10 gl, int w, int h) {
            if (fb != null) {
                fb.dispose();
            }

            if (gl2) {
                fb = new FrameBuffer(w, h); // OpenGL ES 2.0 constructor
            } else {
                fb = new FrameBuffer(gl, w, h); // OpenGL ES 1.x constructor
            }

            if (master == null || isForceRefresh) {

                isForceRefresh = false;

                world = new World();
                world.setAmbientLight(20, 20, 20);

                sun = new Light(world);
                sun.setIntensity(250, 250, 250);

                // Create a texture
                try {
                    Texture texture = new Texture(BitmapHelper.rescale(BitmapHelper.convert(
                            Drawable.createFromStream(getResources().getAssets().open(m_modelName + ".jpg"), null)), 64, 64));
                            //getDrawable(R.mipmap.ic_launcher)), 64, 64));

                    if (TextureManager.getInstance().containsTexture("texture"))
                        TextureManager.getInstance().removeTexture("texture");
                    TextureManager.getInstance().addTexture("texture", texture);
                } catch (IOException e) {
                    e.printStackTrace();
                }

                try {
                    //m_model = loadModel("assets/" + m_modelName + ".3ds", m_modelScale);
                    InputStream opened_model = getResources().getAssets().open(m_modelName + ".3ds");
                    m_model = Object3D.mergeAll(Loader.load3DS(opened_model, m_modelScale));
                } catch (java.io.IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                    return;
                }

                m_model.calcTextureWrapSpherical();
                m_model.setTexture("texture");
                m_model.strip();
                m_model.build();

                world.addObject(m_model);

                Camera cam = world.getCamera();
                cam.moveCamera(Camera.CAMERA_MOVEOUT, 50);
                cam.lookAt(m_model.getTransformedCenter());

                SimpleVector sv = new SimpleVector();
                sv.set(m_model.getTransformedCenter());
                sv.y -= 100;
                sv.z -= 100;
                sun.setPosition(sv);
                MemoryHelper.compact();

                if (master == null) {
                    Logger.log("Saving master Activity!");
                    master = ModelViewer.this;
                }
            }
        }

        public void onSurfaceCreated(GL10 gl, EGLConfig config) {
        }

        public void onDrawFrame(GL10 gl) {
            if (touchTurn != 0) {
                m_model.rotateY(touchTurn);
                touchTurn = 0;
            }

            if (touchTurnUp != 0) {
                m_model.rotateX(touchTurnUp);
                touchTurnUp = 0;
            }

            fb.clear(back);
            world.renderScene(fb);
            world.draw(fb);
            fb.display();

            if (System.currentTimeMillis() - time >= 1000) {
                Logger.log(fps + "fps");
                fps = 0;
                time = System.currentTimeMillis();
            }
            fps++;
        }

        private Object3D loadModel(String filename, float scale) throws UnsupportedEncodingException {

            try {
                InputStream stream = getResources().getAssets().open(filename, 5);
                Object3D[] model = Loader.load3DS(stream, scale);
                Object3D o3d = new Object3D(0);
                Object3D temp = null;
                for (int i = 0; i < model.length; i++) {
                    temp = model[i];
                    temp.setCenter(SimpleVector.ORIGIN);
                    temp.rotateX((float)( -.5*Math.PI));
                    temp.rotateMesh();
                    temp.setRotationMatrix(new Matrix());
                    o3d = Object3D.mergeObjects(o3d, temp);
                    o3d.build();
                }
                return o3d;
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}