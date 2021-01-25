# SSH & Port Forwarding

<br>

## Basic SSH

#### Connect to Host
```bash
ssh USER@HOST_IP -p 2222
```
 - `-p` to specify the port (22 is default) 

#### Connect to Host with Private Key
```bash
ssh -i PRIVATE_KEY USER@HOST_IP
```

#### Copy file(s) to Host
```bash
scp local_file.txt USER@HOST_IP:/tmp/remote_file.txt
```
```bash
scp FILE1 FILE2 USER@HOST_IP:/home/USER/
```

- The `:` is how the `scp` command differentiates between local and remote locations.

#### Copy file from Host
```bash
scp USER@HOST_IP:/tmp/remote_file.txt local_file.txt 
```

<br>

## Local SSH Port Forward

Let's say the remote host is listening on `localhost:3000` and you want to connect to it from your local computer. Perhaps it's a database listening on localhost and you don't want it exposed to the network/internet.

Using a Local Port Forward we can setup a listener on our local computer, which when we connect to will go through the SSH tunnel to the listener on the remote host.

Here is the command that will allow us to do that:

```bash
ssh -L 1337:localhost:3000 USER@REMOTE_HOST_IP
```

This command will setup a listener on your local machine on `localhost:1337`. Connecting to this will be the same as if you connected to `localhost:3000` on the remote host.

<br>

## Remote SSH Port Forward

Let's say you have an application listening on `localhost:9595` on your local computer and your friend wants to connect to your server. However, both you and your friend networks are behind NAT (i.e.two home networks anywhere in the world) so you can't directly connect to each other.

**On your computer:**

```bash
ssh -R 9000:localhost:9595 USER@REMOTE_HOST_IP
```

This command will setup a listener on the remote host on `localhost:9000`. Connecting to the remote host on `localhost:9000` will be the same as if you connected to `localhost:9595` on your local machine.

This situation is now the same as a Local Port Forward. The remote host is now listening on `localhost:9000`. Your friend can now create a new listener on their computer using a Local Port Forward.

**On your friends computer:**

```bash
ssh -L 1337:localhost:9000 USER@REMOTE_HOST_IP
```

<br>

## Remote SSH Port Forward (RDP Example)

Let's say that you want your friend to RDP to your computer. However, you're both in home networks behind NAT.

You can perform a remote port forward to a remote host and expose your RDP listener (0.0.0.0:3389 by default) to the internet. 

### Gateway Ports
The goal is to setup a listener on the remote host on `0.0.0.0:3389`. However, when we do an SSH Port Forward, the default listener is on `127.0.0.1`. To change this and allow it to listen on all interfaces, we need to enabled the `GatewayPorts` options on the SSH Server.

<br>

**On your computer:**

```bash
ssh -R 3389:localhost:3389 USER@REMOTE_HOST_IP
```

Your friend can now RDP to connect directly to the remote host. The connection will then go through the SSH tunnel back to your machine.

**Ensure you have a decent password set before doing this as your PC will be exposed to the internet!**