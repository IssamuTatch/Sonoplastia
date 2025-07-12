import discord
import asyncio
import os

def setup(bot):
    @bot.event
    async def on_voice_state_update(member, before, after):
        # If the user/member is a Bot RETURN
        if member.bot:
            return

        # If user enter in a different channel or a new one continue
        if after.channel is not None and before.channel != after.channel:
            channel = after.channel

            # If Bot is Already in a Voice channel RETURN 
            if channel.guild.voice_client is not None:
                return

            try:
                voice_client = await channel.connect()
                print(f"Entering on voice channel {channel.name}...")

                # Path
                audio_path = "./sound/alo_5.mp3"

                if not os.path.exists(audio_path):
                    print("Audio file not found.")
                    await voice_client.disconnect()
                    return

                # Convert to ffmpeg and play the Audio
                audio_source = discord.FFmpegPCMAudio(audio_path)
                voice_client.play(audio_source)

                # Wait to finish to play then disconnect from channel
                while voice_client.is_playing():
                    await asyncio.sleep(1)

                await voice_client.disconnect()
                channel = None
                print("Exiting after playing the audio file")

            except Exception as e:
                print(f"Error: {e}")