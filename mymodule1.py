def opcc(fname):
    out=[]
    try:
        with open(fname, "r") as file:
            f1 = file.readlines()
            for i in range(0,len(f1),1):
                out.append(f1[i])
    except Exception as e:
        print("Error:", e)
    return out

