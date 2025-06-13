#━━━━━━━━━━━━━━━━━━━━━━
#     Load Modules     
#━━━━━━━━━━━━━━━━━━━━━━

if "add_batchrename" in locals():
    import importlib
    importlib.reload(add_batchrename)
else:
    from . import add_batchrename

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     Register & Unregister     
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register():
    add_batchrename.register()

def unregister():
    add_batchrename.unregister()

if __name__ == "__main__":
    register() 
