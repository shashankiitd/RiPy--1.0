from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PyQt4 import QtGui
import csv
import pyqtgraph
from PyQt4.QtGui import QColor



Tk().withdraw()             
seq_file = askopenfilename() # show an "Open" dialog box and return the path to the selected file


output = open('output.csv','w',newline='')


app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()


## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
layout.setSpacing(1)
w.setLayout(layout)



text_out = QtGui.QTextEdit('Ribosomal Protein CSV : format (Protein Description,Mwt,pI)') # text out widget




data_mwt = []
y_axis = []
x_axis = data_mwt


for record in SeqIO.parse(seq_file, "fasta"):      #for record in SeqIO.parse(seq_file, "fasta"):
    temp_seq=str(record.seq)
    analysis_seq=ProteinAnalysis(temp_seq)
    if ("ribosomal protein" in record.description or "ribosomal subunit" in record.description):
    #if ("ribosomal protein" in record.description or "ribosomal subunit" in record.description or "Ribosomal" in record.description):
        
        if (analysis_seq.molecular_weight() < 20000):
            data_mwt.append('%.2f'%(analysis_seq.molecular_weight()))
            y_axis.append(1)
            
            text_out.setTextColor(QColor('blue'))
            text_out.append(str(len(data_mwt)) + "," + record.description + "," + '%.2f'%(analysis_seq.molecular_weight()) + "," + '%.2f'%(analysis_seq.isoelectric_point()))
            
            
            
        
        #new=sorted(data_mwt)
        #data_mwt.append(list(zip(['%.2f'%(analysis_seq.molecular_weight())])))   
        #print(record.description + "  =  " + '%.2f'%(analysis_seq.molecular_weight()))
        
        csv_write = csv.writer(output)
        #row_wise = zip([record.description],['%.2f'%(analysis_seq.molecular_weight())],['%.2f'%(analysis_seq.isoelectric_point())])
        #data_mwt.append(analysis_seq.molecular_weight())
        row_wise = zip(['%.2f'%(analysis_seq.molecular_weight())],['%.2f'%(analysis_seq.isoelectric_point())])
        for row in row_wise:
            csv_write.writerow(row)
        #csv_write.writerow([record.description + '%.2f'%(analysis_seq.molecular_weight())])
  
pic = QtGui.QLabel(w)

pic.setPixmap(QtGui.QPixmap('logo.png'))


      
text_out.setReadOnly(True)
     
pyqtgraph.setConfigOption('background', 'w')
pyqtgraph.setConfigOption('foreground', 'b')
plot_graph = pyqtgraph.plot(x_axis, y_axis, pen=None, symbol='o')


# Add widgets to the layout in their proper positions #widget-positioning
layout.addWidget(pic, 0, 2, 1, 3)   
#layout.addWidget(info, 0, 2, 1, 3)
#layout.addWidget(text, 0, 2)  
layout.addWidget(text_out, 0, 0, 3, 2)   
layout.addWidget(plot_graph, 1, 2, 2, 4)  


## Display the widget as a new window
w.setWindowTitle('RiPy 1.0')
w.setWindowIcon(QtGui.QIcon('web.png'))
w.show()

## Start the Qt event loop
app.exec_()

