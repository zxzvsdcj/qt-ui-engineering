#include <QApplication>
#include <QMainWindow>
#include <QtGlobal>

#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
#error This fixture targets Qt 5.
#endif

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QMainWindow window;
    window.show();
    return app.exec();
}
