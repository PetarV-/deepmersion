require 'audio'
npy4th = require 'npy4th'

local sound = audio.load(arg[1])
if sound:size(2) > 1 then sound = sound:select(2,1):clone() end
sound:mul(2^-23)
sound = sound:view(1, 1, -1, 1)
sound = sound:resize(1, 1, 22050*20, 1)

npy4th.savenpy(arg[2], sound)

