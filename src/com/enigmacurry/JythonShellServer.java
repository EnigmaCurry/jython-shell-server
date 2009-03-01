package com.enigmacurry;

import org.python.util.PythonInterpreter;
import java.util.*;
import java.net.URL;
import java.net.URLClassLoader;

public class JythonShellServer {
    public static void run_server(int port, Map locals){
        PythonInterpreter p = new PythonInterpreter();
        String jarPath = JythonShellServer.class.getProtectionDomain().getCodeSource().getLocation().getPath();
        p.exec("import sys");
        p.exec("sys.path.append('"+jarPath+"')");
        p.exec("from telnet_shell_server import run_server");
        p.exec("import threading");
        Iterator i = locals.keySet().iterator();
        while(i.hasNext()){
            String key = (String)i.next();
            p.set(key, locals.get(key));
        }
        p.exec("threading.Thread(target=run_server, args=("+port+",locals())).start()");
    }
}
