
import tkinter as tk
from tkinter import ttk

class ParameterTab(ttk.Frame):
    def __init__(self, parent, parameters):
        super().__init__(parent)
        self.parameters = parameters     
        self.tree = ttk.Treeview(self, show='headings', columns=("1", "2"))
        self.tree['show'] = 'headings'

        self.tree.column("1", width=230)
        self.tree.heading("1", text="Parameter")
        self.tree.column("2", width=230)
        self.tree.heading("2", text="Value")
        
        for p in self.parameters:            
            self.tree.insert("", "end", values=(p, self.parameters[p]['value']), tags=self.parameters[p]['type'])              
        
        self.tree.tag_bind('value', '<1>', self.val_edit)
        self.tree.tag_bind('list', '<1>', self.list_edit)
        self.tree.pack(fill='both', expand=True)        
    
    def val_edit(self, event): # value edit event handler
        if self.tree.identify_region(event.x, event.y) == 'cell':
            # the user clicked on a cell
            column = self.tree.identify_column(event.x)  # identify column
            item = self.tree.identify_row(event.y)  # identify item                
            # print(self.tree.item(item)['tags'])
            if column == '#2': # only value column is allowed for editing
                x, y, width, height = self.tree.bbox(item, column) 
                value = self.tree.set(item, column)
                def ok(event):
                    """Change item value."""
                    self.tree.set(item, column, entry.get())
                    entry.destroy()
            else:
                return
        else:
            return
        # display the Entry   
        entry = ttk.Entry(self.tree)  # create edition entry
        entry.place(x=x, y=y, width=width, height=height, anchor='nw')  # display entry on top of cell
        entry.insert(0, value)  # put former value in entry
        entry.bind('<FocusOut>', lambda e: entry.destroy())  
        entry.bind('<Return>', ok)  # validate with Enter
        entry.focus_set()

    def list_edit(self, event): # drop-down list edit event handler
        if self.tree.identify_region(event.x, event.y) == 'cell':
            # the user clicked on a cell
            column = self.tree.identify_column(event.x)  # identify column
            item = self.tree.identify_row(event.y)  # identify item                
            # print(self.tree.item(item)['tags'])
            if column == '#2':
                x, y, width, height = self.tree.bbox(item, column) 
                value = self.tree.set(item, column)
                para_name = self.tree.set(item, '#1')
                options = self.parameters[para_name]['options']
                def ok(event, dummy_1, dummy_2):
                    """Change item value."""
                    self.tree.set(item, column, val.get())
                    val_list.destroy()
            else:
                return
        else:
            return
        # display the drop-down list   
        val = tk.StringVar()
        val_list = ttk.OptionMenu(self.tree, val, options[0], *options)  # create drop-down list
        val_list.place(x=x, y=y, width=width, height=height, anchor='nw')  # display drop-down on top of cell
        val.set(value)  # put former value in entry
        val_list.bind('<FocusOut>', lambda e: val_list.destroy())              
        val.trace('w', ok) # drop-down list value change event 
        val_list.focus_set()

    def output_values(self):
        output = []
        for p in self.tree.get_children():
            output.append(self.tree.item(p)['values'][1])
        return output
    
    def clear(self):
        self.tree.delete(*self.tree.get_children())
        return
    
    def parameter_chg(self, parameters):
        self.clear()
        for p in parameters:
            print(p)            
            self.tree.insert("", "end", values=(p, parameters[p]['value']), tags=parameters[p]['type'])
        return

if __name__ == '__main__':
    root = tk.Tk()
    parameters = {'Parameter 1': {'value':1, 'type':'value', 'options':None},
                  'Parameter 2': {'value':2, 'type':'value', 'options':None},
                  'Parameter 3': {'value':'a', 'type':'list', 'options':('a', 'b', 'c')},
                  'Parameter 4': {'value':'e', 'type':'list', 'options':('e', 'f', 'g')}}
    para_tab = ParameterTab(root, parameters)
    para_tab.pack()
    root.mainloop()