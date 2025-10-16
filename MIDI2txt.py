import mido
import os

def midi_note_to_name(note_num):
    """Convert MIDI note number to note name (e.g., 60 -> C4)"""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note_num // 12) - 1
    name = note_names[note_num % 12]
    return f"{name}{octave}"

files_mid = []
files_txt = []

for file in os.listdir():
    if file.endswith('.mid'):
        files_mid.append(mido.MidiFile(file))
        files_txt.append(open(file.split('.')[0]+'.txt','w'))

for i, file in enumerate(files_mid):
    output = ''
    
    # Write MIDI file header information
    output += f"=== MIDI File Information ===\n"
    output += f"Type: {file.type}\n"
    output += f"Ticks per beat: {file.ticks_per_beat}\n"
    output += f"Number of tracks: {len(file.tracks)}\n"
    output += f"Length (seconds): {file.length}\n\n"
    
    # Process each track
    for track_num, track in enumerate(file.tracks):
        output += f"=== Track {track_num} ===\n"
        output += f"Track name: {track.name if hasattr(track, 'name') else 'Unnamed'}\n"
        output += f"Number of messages: {len(track)}\n\n"
        
        # Track cumulative time
        cumulative_time = 0
        
        for msg in track:
            cumulative_time += msg.time
            
            # Convert time from ticks to seconds
            time_seconds = mido.tick2second(msg.time, file.ticks_per_beat, 500000)  # 500000 is default tempo
            
            # Format the message based on type
            if msg.type == 'note_on':
                note_name = midi_note_to_name(msg.note)
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | NOTE_ON  | Note: {msg.note} ({note_name}) | Velocity: {msg.velocity} | Channel: {msg.channel}\n"
            
            elif msg.type == 'note_off':
                note_name = midi_note_to_name(msg.note)
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | NOTE_OFF | Note: {msg.note} ({note_name}) | Velocity: {msg.velocity} | Channel: {msg.channel}\n"
            
            elif msg.type == 'program_change':
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | PROGRAM_CHANGE | Program: {msg.program} | Channel: {msg.channel}\n"
            
            elif msg.type == 'control_change':
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | CONTROL_CHANGE | Control: {msg.control} | Value: {msg.value} | Channel: {msg.channel}\n"
            
            elif msg.type == 'set_tempo':
                bpm = mido.tempo2bpm(msg.tempo)
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | SET_TEMPO | Tempo: {msg.tempo} microseconds/beat ({bpm:.2f} BPM)\n"
            
            elif msg.type == 'time_signature':
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | TIME_SIGNATURE | {msg.numerator}/{msg.denominator} | Clocks per click: {msg.clocks_per_click} | 32nds per quarter: {msg.notated_32nd_notes_per_beat}\n"
            
            elif msg.type == 'key_signature':
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | KEY_SIGNATURE | Key: {msg.key}\n"
            
            elif msg.type == 'pitchwheel':
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | PITCHWHEEL | Pitch: {msg.pitch} | Channel: {msg.channel}\n"
            
            elif msg.type == 'aftertouch':
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | AFTERTOUCH | Value: {msg.value} | Channel: {msg.channel}\n"
            
            elif msg.type == 'polytouch':
                note_name = midi_note_to_name(msg.note)
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | POLYTOUCH | Note: {msg.note} ({note_name}) | Value: {msg.value} | Channel: {msg.channel}\n"
            
            else:
                # Catch all other message types
                output += f"Time: {cumulative_time} ticks ({time_seconds:.4f}s) | {msg.type.upper()} | {msg}\n"
        
        output += "\n"
    
    files_txt[i].write(output)
    files_txt[i].close()
