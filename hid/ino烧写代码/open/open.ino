#include "DigiKeyboard.h"

void setup() {
  DigiKeyboard.sendKeyStroke(0);

  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT); //按下Win+R建
  DigiKeyboard.delay(200); //等待200毫秒
  DigiKeyboard.println("https://www.baidu.com"); //输入网址
  DigiKeyboard.sendKeyStroke(KEY_ENTER); //回车
  DigiKeyboard.sendKeyStroke(KEY_ENTER); //两次回车以防是中文输入法
}

void loop() {

}
