import sys
from venv import create

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

class Interface( QMainWindow ):
    def __init__( self ):
        self.result_stack = []
        self.operator  = True
        self.start_sig = True
        super().__init__()
        self.initUI()

    def initUI( self ):
        self.title = "계산기 프로그램"
        self.setWindowTitle( self.title )
        self.setGeometry( 1000, 300, 300, 200 )
        self.center()

        main_widget = QWidget( self )
        self.setCentralWidget( main_widget )
        layout_main = QVBoxLayout()
        layout_btn  = QGridLayout()

        # 입력 못하는 self.line #
        self.line = QLineEdit( "" )
        self.line.setReadOnly( True )
        self.line.setAlignment( Qt.AlignRight ) # 오른쪽 정렬
        
        number_btn_dict = {}
        for number in range( 0, 10 ):
            number_btn_dict[ number ] = createButton( str( number ) )
            number_btn_dict[ number ].clicked.connect( lambda state, num = number : self.num_btn_clicked(num))
            if number >0:
                x,y = divmod(9-number, 3)
                layout_btn.addWidget( number_btn_dict[number], x, 2-y )
            elif number==0:
                layout_btn.addWidget( number_btn_dict[number], 3, 0 )
        
        # 사칙연산 버튼 생성 #
        btn_dot   = createButton( "." )
        btn_plus  = createButton( "+" )
        btn_minus = createButton( "-" )
        btn_multy = createButton( "x" )
        btn_div   = createButton( "/" )
        btn_equal = createButton( "=" )
        btn_max   = createButton( "max" )
        btn_min   = createButton( "min" )
        btn_reset = createButton( "C" )
        btn_del   = createButton( "CE" )

        btn_dot.clicked.connect( lambda state,   operation  = ".":   self.btn_operation_clicked( operation ))
        btn_plus.clicked.connect( lambda state,  operation  = "+":   self.btn_operation_clicked( operation ))
        btn_minus.clicked.connect( lambda state, operation  = "-":   self.btn_operation_clicked( operation ))
        btn_multy.clicked.connect( lambda state, operation  = "*":   self.btn_operation_clicked( operation ))
        btn_div.clicked.connect( lambda state,   operation  = "/":   self.btn_operation_clicked( operation ))
        btn_equal.clicked.connect( lambda state, operation  = "=":   self.btn_operation_clicked( operation ))
        btn_max.clicked.connect( lambda state,   operation  = "max": self.btn_stack_clicked( operation ))
        btn_min.clicked.connect( lambda state,   operation  = "min": self.btn_stack_clicked( operation ))
        btn_reset.clicked.connect( lambda state, operation  = "C":   self.btn_clear_clicked( operation ))
        btn_del.clicked.connect( lambda state,   operation  = "CE":  self.btn_clear_clicked( operation ))

        layout_btn.addWidget( btn_dot,   3, 1 )
        layout_btn.addWidget( btn_plus,  0, 3 )
        layout_btn.addWidget( btn_minus, 0, 4 )
        layout_btn.addWidget( btn_multy, 1, 3 )
        layout_btn.addWidget( btn_div,   1, 4 )
        layout_btn.addWidget( btn_equal, 3, 4 )
        layout_btn.addWidget( btn_max,   3, 2 )
        layout_btn.addWidget( btn_min,   3, 3 )
        layout_btn.addWidget( btn_reset, 2, 3 )
        layout_btn.addWidget( btn_del,   2, 4 )

        layout_main.addWidget( self.line )
        layout_main.addLayout( layout_btn )
        
        main_widget.setLayout( layout_main )
        
        self.show()

    def num_btn_clicked( self, num ):
        if self.start_sig == True :
            self.line.clear()
            self.start_sig = False

        line = self.line.text()
        line += str( num )
        self.line.setText( line )
        self.operator = False

    def btn_operation_clicked(self, operation):
        if not self.operator:
            if operation == "=":
                line = self.line.text()
                result = eval(line)
                self.line.setText( str( result ))
                self.result_stack.append( result )
                self.start_sig = True
            else :    
                line = self.line.text()
                line += operation
                self.line.setText( line )
                self.operator = True

    def btn_equal_clicked( self ):
        if not self.operator:
            line = self.line.text()
            result = eval(line)
            self.line.setText( str( result ))
            self.result_stack.append( result )

    def btn_clear_clicked( self, operation ):
        self.line.setText("")
        if operation == "CE":
            self.result_stack = []
        
    def btn_stack_clicked( self, operation ):
        self.line.setText("")
        if len( self.result_stack ) == 0:
            return
        elif operation == "max":
            result = max( self.result_stack )
            self.line.setText( str( result ) )
        else :
            result = min( self.result_stack )
            self.line.setText( str( result ) )

    # (py)qt에서 약속된 지정함수
    def keyPressEvent( self, e ):
        if e.key() == 16777220 or e.key() == 16777221 or e.key() == 61 :
            self.btn_operation_clicked( "=" )
        elif e.key() >= 48 and e.key() <= 57:
            self.num_btn_clicked( chr( e.key() ))
        elif e.key() == 42 or e.key() == 43 or e.key() == 45 or e.key() == 46 or e.key() == 47:
            self.btn_operation_clicked( chr( e.key() ))

    # 추가할 것 중앙 정렬 코드
    def center( self ):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter( cp )
        self.move( qr.topLeft() )

class createButton( QToolButton ):
    def __init__( self, text ):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred) # 버튼의 사이즈 규정 결정
        self.setText( text )


if __name__ == "__main__":
    app = QApplication( sys.argv )
    calculator = Interface()
    app.exec_()