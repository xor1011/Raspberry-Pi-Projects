/*Program written in C++ by Martin Johnson
 * program is desgined to allow you to execute a command at a specific time
 * originally designed to be a poweroff/sleeptimer I changed my mind
 * has a beep noise so it can be used as a timer for you oven or something
 * I am releasing this to the Raspberry Pi/Linux/Anyone community to do with what you please
 * Use this software at your own discretion. I accept no responsibility for how you use it
 * This is open source. No license implied
 * You're welcome
 */

#include "mainwindow.h" //Lazy file creation
#include "ui_mainwindow.h"

//void sleepTimer();
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{

    ui->setupUi(this);
    QPushButton *button=ui->pushButton;
    connect(button, SIGNAL(released()), this, SLOT(sleepTimer())); //the button does the heavy lifting

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::sleepTimer(){//not a sleeptimer....Anymore.....

    QTimer *timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, &MainWindow::timerSlot);
        timer->start(400);//kind of randomly chosen. Works



}
//Everything happens here
void MainWindow::timerSlot(){
    QTime ct=QTime::currentTime();
    QTime st=ui->timeEdit->time();
    QString cmd=ui->lineEdit->text();
    //lets get the difference between the time and timer's time
    int mdif=st.minute()-ct.minute();
    int hdif=st.hour()-ct.hour();
    if (st.hour()<=ct.hour() && st.minute()<ct.minute()){ //if its earlier than current. Make tomorrow
        mdif*=-1;
        hdif+=23;
    }
    int sdif=59-st.second()-ct.second();//so it counts down.
    QString timeLeft="";
    timeLeft.append(QString::number(hdif));
    timeLeft.append(":");
    timeLeft.append(QString::number(mdif-1)); //sigh -1
    timeLeft.append(":");
    if (sdif==60 && mdif>0)timeLeft.append("00"); //may not be needed, but I needed it earlier
    else timeLeft.append(QString::number(sdif));
    ui->label->setText(timeLeft);
    if (hdif<=0 && mdif<=0){ //we're down to zero
        ui->label->setText("Complete"); //Yeah
        for (int a=0; a<=2; a++) //beep 3 times
            system("mpg123 /home/pi/Music/beep.mp3");
        system(cmd.toUtf8()); //old school C for the win
        exit(0); //lets get out of here so we don't have to make a boolean to stop the beeps and system commands
    }
}
