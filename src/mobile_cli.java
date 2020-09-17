package com.company.pointscan;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Build;
import android.os.Bundle;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.os.Environment;
import android.text.format.Time;
import android.util.Log;
import android.view.View;

import android.view.Menu;
import android.view.MenuItem;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.text.DateFormat;
import java.time.Instant;
import java.util.Date;
import java.util.List;

import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.TextView;
import android.widget.Toast;


import com.company.pointscanner.R;

import org.apache.poi.hssf.record.formula.functions.T;
import org.apache.poi.hssf.usermodel.HSSFCellStyle;
import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.hssf.util.HSSFColor;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import java.util.Calendar;
import java.util.Locale;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Context context;
    WifiManager wifiManager;
    TextView errors;
    Button Scan, Write;
    ListView lv;
    SimpleAdapter adapter;
    private final int REQUEST_CODE_PERMISSION_FINE_LOC = 1;
    private final int REQUEST_CODE_PERMISSION_WRITE = 2;
    List<ScanResult> results;
    String sense[], prom[];
    String date;
   // Date date;
    String fileName;
    File file;
    DateFormat df;
    EditText editX, editY;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        context = getApplicationContext();
        wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
        errors = findViewById(R.id.errors);
        Scan = findViewById(R.id.Scan);
        Write = findViewById(R.id.Write);
        lv = findViewById(R.id.list);
        editX = findViewById(R.id.editX);
        editY = findViewById(R.id.editY);
        String mydate = java.text.DateFormat.getDateInstance().format(Calendar.getInstance().getTime());
       fileName = "Протокол измерений " + Build.MODEL + " " + mydate + ".xls";
       // fileName = "Proto.xls";
       // Date calendar = c
        Scan.setOnClickListener((View.OnClickListener) this);
        Write.setOnClickListener((View.OnClickListener) this);
        onRequestPermissionsResult();
    }

    public static boolean hasPermissions(Context context, String... permissions) {
        if (context != null && permissions != null) {
            for (String permission : permissions) {
                if (ActivityCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED) {
                    return false;
                }
            }
        }
        return true;
    }

    public void onRequestPermissionsResult() {
        int PERMISSION_ALL = 1;
        String[] PERMISSIONS = {
                android.Manifest.permission.WRITE_EXTERNAL_STORAGE,
                android.Manifest.permission.ACCESS_FINE_LOCATION,
        };

        if (!hasPermissions(this, PERMISSIONS)) {
            while (!hasPermissions(this, PERMISSIONS))
                ActivityCompat.requestPermissions(this, PERMISSIONS, PERMISSION_ALL);
        }
    }

    private void scanSuccess() {
        results = wifiManager.getScanResults();
        int r = results.size();
        int i = 0, v = 0;
        prom = new String[r];
        while (i < r) {
            if (results.get(i).level >= -75) {
                prom[v] = ("SSID: " + results.get(i).SSID + "\r\nMAC: " + results.get(i).BSSID + "\r\nRSSI: " + results.get(i).level);
                i++;
                v++;
            } else i++;
        }
        sense = new String[v];
        i = 0;
        while (i < v) {
            sense[i] = (prom[i]);
            i++;
        }
        lv.setAdapter(new ArrayAdapter<>(this, R.layout.row, sense));
        errors.setText("");
    }

    private void scanFailure() {
        if (results == null) errors.setText("Ошибка поиска");
        else errors.setText("Нет новых результатов");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void onClick(View v) {

        switch ((v.getId())) {
            case R.id.Scan: {
                BroadcastReceiver wifiScanReceiver = new BroadcastReceiver() {
                    @RequiresApi(api = Build.VERSION_CODES.M)
                    @Override
                    public void onReceive(Context c, Intent intent) {
                        boolean success = intent.getBooleanExtra(WifiManager.EXTRA_RESULTS_UPDATED, false);
                        if (success) {
                            scanSuccess();
                        } else {
                            scanFailure();
                        }
                    }
                };
                IntentFilter intentFilter = new IntentFilter();
                intentFilter.addAction(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION);
                context.registerReceiver(wifiScanReceiver, intentFilter);

                boolean success = wifiManager.startScan();
                if (success) {
                    scanSuccess();
                } else scanFailure();
                break;
            }
            case R.id.Write: {
                File file = new File(context.getExternalFilesDir("/storage/Documents"), fileName);
                if (!file.exists() || file == null)
                {Toast.makeText(getApplicationContext(), "Меня не существует!", Toast.LENGTH_SHORT).show();
                    createExcelFile(this, fileName);
                break;}
                else { Toast.makeText(getApplicationContext(), "Я есть!", Toast.LENGTH_SHORT).show();
                    try {saveExcelFile(this, fileName);
                           } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }

    private boolean createExcelFile(Context context, String fileName) {

        if (!isExternalStorageWritable()) {
            Toast.makeText(getApplicationContext(), "Хранилище недоступно для записи", Toast.LENGTH_SHORT).show();
            return false;
        }

        boolean writing = false;

        Workbook wb = new HSSFWorkbook();

        Cell c = null;

        CellStyle cs = wb.createCellStyle();
        cs.setFillForegroundColor(HSSFColor.TAN.index);
        cs.setFillPattern(HSSFCellStyle.SOLID_FOREGROUND);

        Sheet sheet1 = null;
        sheet1 = wb.createSheet("Протокол измерений" + Build.MANUFACTURER + " " + Build.PRODUCT);

        Row rows[] = new Row[10000];
        rows[0] = sheet1.createRow(0);
        c = rows[0].createCell(0);
        c.setCellValue(Build.MANUFACTURER + " " + Build.PRODUCT);

        rows[1] = sheet1.createRow(1);
        c = rows[1].createCell(0);
        c.setCellValue("Координата X");
        c.setCellStyle(cs);

        c = rows[1].createCell(1);
        c.setCellValue("Координата Y");
        c.setCellStyle(cs);

        c = rows[1].createCell(2);
        c.setCellValue("SSID");
        c.setCellStyle(cs);

        c = rows[1].createCell(3);
        c.setCellValue("MAC");
        c.setCellStyle(cs);

        c = rows[1].createCell(4);
        c.setCellValue("RSSI");
        c.setCellStyle(cs);

        sheet1.setColumnWidth(0, (15 * 220));
        sheet1.setColumnWidth(1, (15 * 220));
        sheet1.setColumnWidth(2, (15 * 500));
        sheet1.setColumnWidth(3, (15 * 300));
        sheet1.setColumnWidth(4, (15 * 100));

        int i = 0;
        int v = 2;
        int qq = 0;
        if (!results.isEmpty()) qq = results.size();
        if (qq != 0) {
            while (i < qq) {
                if (results.get(i).level >= -75) {
                    rows[v] = sheet1.createRow(v);
                    c = rows[v].createCell(0);
                    c.setCellValue(editX.getText().toString());
                    c = rows[v].createCell(1);
                    c.setCellValue(editY.getText().toString());
                    c = rows[v].createCell(2);
                    c.setCellValue(results.get(i).SSID);
                    c = rows[v].createCell(3);
                    c.setCellValue(results.get(i).BSSID);
                    c = rows[v].createCell(4);
                    c.setCellValue(results.get(i).level);
                    i++;
                    v++;
                } else i++;
            }

            //    file = context.getFileStreamPath(fileName);
            //   if (!file.exists()) {
            file = new File(context.getExternalFilesDir("/storage/Documents"), fileName);
            FileOutputStream os = null;

            try {
                os = new FileOutputStream(file);
                wb.write(os);
               // wb.close();
                Toast.makeText(getApplicationContext(), "Записываю файл" + file, Toast.LENGTH_SHORT).show();
                writing = true;
            } catch (IOException e) {
                Toast.makeText(getApplicationContext(), "Ошибка записи файла" + file, Toast.LENGTH_SHORT).show();
            } catch (Exception e) {
                Toast.makeText(getApplicationContext(), "Не получилось сохранить файл" + file, Toast.LENGTH_SHORT).show();
            } finally {
                try {
                    if (null != os)
                        os.close();
                } catch (Exception ex) {
                }
            }

            Toast.makeText(getApplicationContext(), "Файл сохранен", Toast.LENGTH_SHORT).show();
            return writing;
        } else {
            //Toast.makeText(getApplicationContext(), "Нет данных", Toast.LENGTH_SHORT).show();
            return writing;
        }
    }

    private boolean saveExcelFile(Context context, String fileName) throws Exception {

        if (!isExternalStorageWritable()) {
            Toast.makeText(getApplicationContext(), "Хранилище недоступно для записи", Toast.LENGTH_SHORT).show();
            return false;
        }

        boolean writing = false;

        file = new File(context.getExternalFilesDir("/storage/Documents"), fileName);
        FileInputStream is = new FileInputStream(file);

        Workbook wb = new HSSFWorkbook(is);
        Sheet sheet1 = wb.getSheetAt(0);

        int v = sheet1.getPhysicalNumberOfRows() + 1;
        Toast.makeText(getApplicationContext(), Integer.toString(v), Toast.LENGTH_SHORT).show();
        Row rows[] = new Row[10000];

        Cell c = null;

        CellStyle cs = wb.createCellStyle();
        cs.setFillForegroundColor(HSSFColor.TAN.index);
        cs.setFillPattern(HSSFCellStyle.SOLID_FOREGROUND);

        int i = 0;
        int qq = 0;
        if (!results.isEmpty()) qq = results.size();
        if (qq != 0) {
            while (i < qq) {
                if (results.get(i).level >= -75) {
                    rows[v] = sheet1.createRow(v);
                    c = rows[v].createCell(0);
                    c.setCellValue(editX.getText().toString());
                    c = rows[v].createCell(1);
                    c.setCellValue(editY.getText().toString());
                    c = rows[v].createCell(2);
                    c.setCellValue(results.get(i).SSID);
                    c = rows[v].createCell(3);
                    c.setCellValue(results.get(i).BSSID);
                    c = rows[v].createCell(4);
                    c.setCellValue(results.get(i).level);
                    i++;
                    v++;
                } else i++;
            }

            FileOutputStream os = null;

            try {
                os = new FileOutputStream(file);
                wb.write(os);
                // wb.close();
                Toast.makeText(getApplicationContext(), "Записываю файл" + file, Toast.LENGTH_SHORT).show();
                writing = true;
            } catch (IOException e) {
                Toast.makeText(getApplicationContext(), "Ошибка записи файла" + file, Toast.LENGTH_SHORT).show();
            } catch (Exception e) {
                Toast.makeText(getApplicationContext(), "Не получилось сохранить файл" + file, Toast.LENGTH_SHORT).show();
            } finally {
                try {
                    if (null != os)
                      os.close();  is.close();
                } catch (Exception ex) {
                }
            }

            Toast.makeText(getApplicationContext(), "Файл сохранен", Toast.LENGTH_SHORT).show();
            return writing;
        } else {
            //Toast.makeText(getApplicationContext(), "Нет данных", Toast.LENGTH_SHORT).show();
            return writing;
        }
    }

    public boolean isExternalStorageWritable () {
        String state = Environment.getExternalStorageState();
        if (Environment.MEDIA_MOUNTED.equals(state)) {
            return true;
        }
        return false;
    }
}
