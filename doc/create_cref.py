from xml.dom.minidom import parse
import os, sys
try:
    import cStringIO as stringio
except ImportError:
    import io as stringio

def prepare_text (text):
    newtext = ""
    tmptext = ""
    text = text.replace ("\"", "\\\"")
    lines = text.split ("\n")
    nn = "normalize" in text
        
    for l in lines:
        l = l.strip ().replace ("::", "")
        if l.startswith ("|"):
            # Peserve spacings.
            l = l.replace (":const:", "       ")
            l = l.replace (":class:", "       ")
            l = l.replace (":meth:", "      ")
            l = l.replace (":ref:", "     ")
            l = l.replace (":exc:", "     ")
            l = l.replace ("`", " ")
        else:
            l = l.replace (":const:", "")
            l = l.replace (":class:", "")
            l = l.replace (":meth:", "")
            l = l.replace (":ref:", "")
            l = l.replace (":exc:", "")
            l = l.replace ("`", "")
        l = l.replace (".. note::", "NOTE:")

        tmptext += l + "\\n"
    tmptext = tmptext.replace ("\\n", "")
    while len (tmptext) > 1900:
        # Split after 2000 characters to avoid problems with the Visual
        # C++ 2048 character limit.
        newtext += tmptext[:1900] + "\" \\\n\""
        tmptext = tmptext[1900:]
    newtext += tmptext
    return newtext

def create_cref (dom, buf):
    module = dom.getElementsByTagName ("module")[0]
    modname = module.getAttribute ("name")
    tmp = modname.split (".")[-1]
    headname = tmp.upper()
    docprefix = "DOC_%s_" % headname
    desc = ""
    node = module.getElementsByTagName ("desc")
    if node and node[0].firstChild:
        desc = node[0].firstChild.nodeValue
        desc = prepare_text (desc)
    
    buf.write ("#ifndef _PYGAME2_DOC%s_H_\n" % headname)
    buf.write ("#define _PYGAME2_DOC%s_H_\n\n" % headname)
    buf.write ("#define DOC_%s \"%s\"\n" % (headname, desc))
    
    create_func_refs (module, docprefix, buf)
    create_class_refs (module, docprefix, buf)
    
    buf.write ("\n#endif\n")

def create_func_refs (module, docprefix, buf):
    funcs = module.getElementsByTagName ("func")
    for func in funcs:
        name = func.getAttribute ("name").upper ()
        call = ""
        node = func.getElementsByTagName ("call")
        if node and node[0].firstChild:
            call = node[0].firstChild.nodeValue + "\n"
        node = func.getElementsByTagName ("desc")
        desc = call
        if node and node[0].firstChild:
            desc += node[0].firstChild.nodeValue
        desc = prepare_text (desc)
        buf.write ("#define %s \"%s\"\n" % (docprefix + name, desc))
    
def create_class_refs (module, docprefix, buf):
    classes = module.getElementsByTagName ("class")
    for cls in classes:
        name = cls.getAttribute ("name").upper ()
        node = cls.getElementsByTagName ("constructor")
        constructor = "TODO\n"
        if node and node[0].firstChild:
            constructor = node[0].firstChild.nodeValue + "\n"
        desc = constructor
        node = cls.getElementsByTagName ("desc")
        if node and node[0].firstChild:
            desc += node[0].firstChild.nodeValue
        desc = prepare_text (desc)
        buf.write ("#define %s \"%s\"\n" % (docprefix + name, desc))

        attrs = cls.getElementsByTagName ("attr")
        attrprefix = docprefix + name + "_"
        for attr in attrs:
            create_attr_ref (attr, attrprefix, buf)

        methods = cls.getElementsByTagName ("method")
        methodprefix = attrprefix
        for method in methods:
            create_method_ref (method, methodprefix, buf)

def create_attr_ref (attr, prefix, buf):
    name = attr.getAttribute ("name").upper ()
    desc = ""
    node = attr.getElementsByTagName ("desc")
    if node and node[0].firstChild:
        desc = node[0].firstChild.nodeValue
    desc = prepare_text (desc)
    buf.write ("#define %s \"%s\"\n" % (prefix + name, desc))
    
def create_method_ref (method, prefix, buf):
    name = method.getAttribute ("name").upper ()
    call = ""
    desc = ""
    node = method.getElementsByTagName ("call")
    if node and node[0].firstChild:
        call = node[0].firstChild.nodeValue + "\n"
    node = method.getElementsByTagName ("desc")
    if node and node[0].firstChild:
        desc += node[0].firstChild.nodeValue
    desc = prepare_text (desc)
    call = prepare_text (call)
    buf.write ("#define %s \"%s\\n\\n%s\"\n" % (prefix + name, call, desc))

def create_c_header (infile, outfile):
    try:
        dom = parse (infile)
        buf = stringio.StringIO ()
        create_cref (dom, buf)
        f = open (outfile, "w")
        f.write (buf.getvalue ())
        f.flush ()
        f.close ()
    except Exception:
        raise
        #print (sys.exc_info()[1])

if __name__ == "__main__":
    if len (sys.argv) < 2:
        print ("usage: %s file.xml" % sys.argv[0])
        sys.exit (1)
    dom = parse (sys.argv[1])
    buf = stringio.StringIO ()
    create_cref (dom, buf)
    print (buf.getvalue ())
