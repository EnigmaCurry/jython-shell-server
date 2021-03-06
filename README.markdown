# Jython Shell Server

This library embeds a network-reachable, interactive, Jython shell into any Java application. Once you instantiate the server, you can telnet directly into your java application from any computer on the network and be presented with a Jython [REPL](http://en.wikipedia.org/wiki/REPL).

## Building

You'll need:

1. a Java SDK (tested on 1.6)
2. [ant](http://ant.apache.org)
3. [Jython](http://www.jython.org) (tested on 2.5b1)

Copy your jython jar into the lib folder and run 'ant'. This builds JythonShellServer.jar which you can include in your application's CLASSPATH.

## Known issues

This library is not threadsafe, yet. You can log into the REPL more than once, but due to the way the console is printed, the first connection will stop working when you log in through the second connection. 

## Usage

1. Include your Jython jar file and JythonShellServer.jar in your application's CLASSPATH.
2. Somewhere in your application run com.enigmacurry.JythonShellServer.run_server(7000);
3. run "telnet localhost 7000" and you should be connected to the Jython REPL.

If you want readline support, install [rlwrap](https://github.com/hanslub42/rlwrap) and instead run "rlwrap telnet localhost 7000".

## Example

Here's an example of how you would integrate Jython Shell Server into an off-the-shelf java application. Let's use one of the most popular java projects here on github: [IRCcat](http://github.com/RJ/irccat), which is a nifty IRC bot that responds to messages netcat'd to it.

1. Download the IRCcat sources, run "git clone git://github.com/RJ/irccat.git"
2. Copy the jython jar file to the libs directory
3. Copy the JythonShellServer.jar to the libs directory
4. Instantiate Jython Shell Server inside IRCCat.java inside the IRCCat constructor:

```
public IRCCat(XMLConfiguration c) throws Exception {
    //Load Jython shell server
    java.util.Map localVars = new java.util.HashMap();
    localVars.put("IRCCat",this);
    com.enigmacurry.JythonShellServer.run_server(7000, localVars);
}
```

localVars is a map of variable names that you want to have available to you inside the Jython REPL. In the above example we are placing the main IRCCat object (referenced by 'this') as a variable in Jython called "IRCCat".

5. Build IRCCat by running "ant".
6. Setup your own irccat.xml file (based on the one in the examples directory).
7. run IRCCat "ant -Dconfigfile=irccat.xml run"
8. now telnet into the application: "telnet localhost 7000".

Supposing you set in your irccat.xml file for IRCCat to join a channel called "#TestIRCCat" you can now play around with the bot inside the Jython REPL:

![Jython Shell Server REPL](https://github.com/EnigmaCurry/jython-shell-server/raw/59d09734b826a7e427ba408dece13339e2e39c66/doc/IRCcatREPL.png)

and you can see the effect in the IRC channel:

![IRCcat in channel](https://github.com/EnigmaCurry/jython-shell-server/raw/59d09734b826a7e427ba408dece13339e2e39c66/doc/TestIRCcat.png)

