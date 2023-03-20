import argparse
import asyncio
import json
import logging
import os
import random
import platform
import websockets
import requests

from aiortc import (
    RTCIceCandidate,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
    RTCRtpSender,
)
from aiortc.contrib.media import MediaPlayer
from aiortc.contrib.signaling import ApprtcSignaling

async def run(pc, player, signaling):
    def add_tracks():
        if player and player.audio:
            pc.addTrack(player.audio)

        if player and player.video:
            pc.addTrack(player.video)
            # this forces h264 as video codec
            # raspi 3 not powerful enough to run a useful vp8 stream
            caps = RTCRtpSender.getCapabilities('video')
            prefs = list(filter(lambda x: x.name == 'H264', caps.codecs))
            transceiver = pc.getTransceivers()[0]
            transceiver.setCodecPreferences(prefs)

    @pc.on("track")
    def on_track(track):
        # received tracks are discarded, to avoid unecessary load on the cpu
        print("Track %s received" % track.kind)

    # connect to websocket and join
    params = await signaling.connect()

    if params["is_initiator"] == "true":
        # send offer
        add_tracks()
        await pc.setLocalDescription(await pc.createOffer())
        await signaling.send(pc.localDescription)

    # consume signaling
    while True:
        obj = await signaling.receive()

        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)

            if obj.type == "offer":
                # send answer
                add_tracks()
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)
        elif isinstance(obj, RTCIceCandidate):
            pc.addIceCandidate(obj)
        elif isinstance(obj, str):
            # print debug messages
            print(obj);
        elif obj is None:
            print("Exiting")
            break


if __name__ == "__main__":
    # parse arguments given when starting the script
    parser = argparse.ArgumentParser(description="AppRTC")
    parser.add_argument("room", nargs="?")
    parser.add_argument("--play-from", default="/dev/video0", help="Video device path to get video from. (Default: /dev/video0)"),
    parser.add_argument("--framerate", default="20", help="Framerate for video device. (Default: 20)"),
    parser.add_argument("--resolution", default="640x480", help="Resolution for video device. (Default: 640x480)"),
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()

    # if no room id is given, join a random room
    if not args.room:
        args.room = "".join([random.choice("0123456789") for x in range(10)])

    r = requests.post('http://' + os.environ['PUSH_HOST'] + '/api/send-msg', json ={"title":"Camera Stream", "text":"Webcam was triggered. Room: " + args.room, "url":"https://appr.tc/r/" + args.room})
    print(args.room, flush=True)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # create apprtc signaling and peer connection
    signaling = ApprtcSignaling(args.room)
    pc = RTCPeerConnection()

    # create media source from arguments
    player = MediaPlayer(args.play_from, format="v4l2", options={"framerate": args.framerate, "video_size": args.resolution})

    # run event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            run(pc=pc, player=player, signaling=signaling)
        )
    except KeyboardInterrupt:
        pass
    finally:
        # cleanup signaling and peer connection on close
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())
