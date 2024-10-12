import tkinter as tk
from tkinter import font, filedialog
import stage1, stage2, stage3, stage4  


def upload_file_and_execute(stage_function, stage_number):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        result = stage_function(file_path)
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, result)
        

def upload_two_files_and_compare(compare_function):
    file_path1 = filedialog.askopenfilename(title="Select the first graph file", filetypes=[("Text files", "*.txt")])
    file_path2 = filedialog.askopenfilename(title="Select the second graph file", filetypes=[("Text files", "*.txt")])

    if file_path1 and file_path2:
        graph1 = stage2.read_graphs_from_file(file_path1)[0]  
        graph2 = stage2.read_graphs_from_file(file_path2)[0]  

        result = compare_function(graph1, graph2)
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, result)


root = tk.Tk()
root.title("Multigraph Analysis Tool")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width * 0.9)
window_height = int(screen_height * 0.9)

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2


root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")



output_text_font = font.Font(family="Helvetica", size=13, weight="bold")

custom_font = font.Font(family="Helvetica", size=24, weight="bold")
small_font = font.Font(family="Helvetica", size=12)

description_label = tk.Label(root, text="Welcome to the Multigraph Analysis Tool. Select a stage and upload a file to process.", font=small_font, wraplength=500)
description_label.pack()


output_text = tk.Text(root, height=30, width=150, font=output_text_font)
output_text.pack()

default_output_text = (
    " Select a stage and upload a file to begin analysis. \n"
    "\n"
    " Stage 1 calculates the size of the graph. Size is defined as a sum of vertices and edges \n"
    "\n"
    " Stage 2 calculates the distance (Hamming distance) as number of differencies between graphs (details in the report) \n"
    "\n"
    " Stage 3 calculates maximal clique (size defined in stage 1) \n"
    "\n"
    " Stage 4 calculate maximal common subgraph \n"
    "\n"
    " Remark 1: please, be informed that the wrong format of the txt. file can cause the malfunction of the program. Prepare the file with right format \n"
    "\n"
    " Remark 2: stage 2 always return the right distance but if the matrix is not adjacency matrix or will have numbers on the main diagonal, the output matrix will not be accurate but the result will be correct.\n"
    "\n"
    " Remark 3: stage 4 works perfectly for ordinary graphs but with some multigraphs it may do mistakes \n"
    "\n"
    " Remark 4: please, open application on the fullscreen mode to see all options of the program. \n"

)

output_text.insert(tk.END, default_output_text)


stage1_button = tk.Button(root, text="Stage 1: One file", command=lambda: upload_file_and_execute(stage1.process, 1))
stage1_button.pack()

stage2_button = tk.Button(root, text="Stage 2: One file", command=lambda: upload_file_and_execute(stage2.process, 2))
stage2_button.pack()
compare_two_files_stage3_button = tk.Button(root, text="Stage 2: 2 files", command=lambda: upload_two_files_and_compare(stage2.compare_two_graphs))
compare_two_files_stage3_button.pack()  


stage3_button = tk.Button(root, text="Stage 3: One file ", command=lambda: upload_file_and_execute(stage3.process, 3))
stage3_button.pack()

stage4_button = tk.Button(root, text="Stage 4: One file", command=lambda: upload_file_and_execute(stage4.process, 4))
stage4_button.pack()

compare_two_files_stage4_button = tk.Button(root, text="Stage 4: 2 files", command=lambda: upload_two_files_and_compare(stage4.compare_two_graphs))
compare_two_files_stage4_button.pack()




root.mainloop()
