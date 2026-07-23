import customtkinter as ctk
from tkinter import filedialog
from src.workspaces.research_workspace import ResearchWorkspace

class ResearchWorkspacesWindow(ctk.CTkToplevel):
    def __init__(self, master, service, brief_service):
        super().__init__(master)
        self.service = service
        self.brief_service = brief_service
        self.title("Research Workspaces")
        self.geometry("950x760")
        self.minsize(760, 600)
        self.transient(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(self, text="Research Workspaces", font=("Segoe UI", 22, "bold"), anchor="w").grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))
        add = ctk.CTkFrame(self)
        add.grid(row=1, column=0, sticky="ew", padx=15, pady=6)
        add.grid_columnconfigure(0, weight=1)
        self.title_entry = ctk.CTkEntry(add, placeholder_text="Research workspace title")
        self.title_entry.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.focus_entry = ctk.CTkEntry(add, placeholder_text="Research focus")
        self.focus_entry.grid(row=0, column=1, sticky="ew", padx=8, pady=8)
        ctk.CTkButton(add, text="Add Workspace", command=self.add).grid(row=0, column=2, padx=8, pady=8)
        self.list = ctk.CTkScrollableFrame(self)
        self.list.grid(row=2, column=0, sticky="nsew", padx=15, pady=(6, 15))
        self.refresh()
    def add(self):
        if self.title_entry.get().strip():
            self.service.add(self.title_entry.get(), self.focus_entry.get())
            self.title_entry.delete(0, "end"); self.focus_entry.delete(0, "end"); self.refresh()
    def refresh(self):
        for widget in self.list.winfo_children(): widget.destroy()
        for item in self.service.workspaces:
            card = ctk.CTkFrame(self.list); card.pack(fill="x", padx=5, pady=6); card.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(card, text=f"{item.title}\n{item.status}   Focus: {item.focus or 'Not set'}", font=("Segoe UI", 13, "bold"), justify="left", anchor="w").grid(row=0, column=0, sticky="ew", padx=10, pady=8)
            ctk.CTkButton(card, text="Open", width=75, command=lambda value=item: WorkspaceEditor(self, value, self.service, self.refresh)).grid(row=0, column=1, padx=5, pady=8)
            ctk.CTkButton(card, text="Export Brief", width=95, command=lambda value=item: self.export_brief(value)).grid(row=0, column=2, padx=5, pady=8)
            ctk.CTkButton(card, text="Remove", width=75, command=lambda value=item.workspace_id: self.remove(value)).grid(row=0, column=3, padx=(5, 10), pady=8)
    def remove(self, workspace_id):
        self.service.remove(workspace_id); self.refresh()
    def export_brief(self, item):
        path=filedialog.asksaveasfilename(parent=self,title="Export Discovery Research Brief",defaultextension=".txt",initialfile="OpportunityLab-Discovery-Brief.txt",filetypes=[("Text files","*.txt")])
        if path: self.brief_service.export(item,path)

class WorkspaceEditor(ctk.CTkToplevel):
    def __init__(self, master, item, service, on_save):
        super().__init__(master); self.item=item; self.service=service; self.on_save=on_save
        self.title("Research Workspace"); self.geometry("780x720"); self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure((3,5,7), weight=1)
        self.title_entry=ctk.CTkEntry(self); self.title_entry.grid(row=0,column=0,sticky="ew",padx=15,pady=(15,5)); self.title_entry.insert(0,item.title)
        self.status=ctk.StringVar(value=item.status); ctk.CTkOptionMenu(self,values=list(ResearchWorkspace.STATUSES),variable=self.status).grid(row=1,column=0,sticky="w",padx=15,pady=5)
        self.focus=ctk.CTkEntry(self,placeholder_text="Research focus"); self.focus.grid(row=2,column=0,sticky="ew",padx=15,pady=5); self.focus.insert(0,item.focus)
        self.questions=self._box("Research questions",3,item.questions)
        self.findings=self._box("Findings and evidence",5,item.findings)
        self.conclusions=self._box("Conclusions and next actions",7,item.conclusions)
        ctk.CTkButton(self,text="Save Workspace",command=self.save).grid(row=9,column=0,sticky="e",padx=15,pady=15)
    def _box(self,label,row,text):
        ctk.CTkLabel(self,text=label,anchor="w",font=("Segoe UI",13,"bold")).grid(row=row-1,column=0,sticky="ew",padx=15,pady=(8,2))
        box=ctk.CTkTextbox(self,wrap="word"); box.grid(row=row,column=0,sticky="nsew",padx=15,pady=4); box.insert("1.0",text); return box
    def save(self):
        self.service.update(self.item.workspace_id,title=self.title_entry.get(),focus=self.focus.get(),status=self.status.get(),questions=self.questions.get("1.0","end"),findings=self.findings.get("1.0","end"),conclusions=self.conclusions.get("1.0","end"))
        self.on_save(); self.destroy()
