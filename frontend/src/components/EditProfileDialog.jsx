import {Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField} from "@mui/material";

export default function EditProfileDialog(
    {
        openProfile,
        setOpenProfile,
        profileData,
        setProfileData,
        updateProfileMutation,
    }
){
    return(
        <>
        <Dialog open={openProfile} onClose={() => setOpenProfile(false)}
     fullWidth
    >
    <DialogTitle
      sx={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
    Edit Profile

    <Button
      onClick={() => setOpenProfile(false)}
      sx={{
        minWidth: 0,
        color: "gray",
        fontSize: "13px",
      }}
    >
    ✕
    </Button>
    </DialogTitle>

    <DialogContent
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 2,
        mt: 3,

      }}
    >

    <TextField
      label="New Name"
      size="small"
      value={profileData.name}
      onChange={(e) =>
        setProfileData({ ...profileData, name: e.target.value })
      }
      sx={{
        "& .MuiInputBase-root": {
          fontSize: "14px",
          borderRadius: "10px",
        },
        "& .MuiInputLabel-root": {
          fontSize: "13px",
        },
      "& .MuiInputLabel-shrink": {
        transform: "translate(11px, -6px) scale(0.75)",
      },
      }}
    />

    <TextField
      label="Old Password"
      type="password"
      size="small"
      value={profileData.oldPassword}
      onChange={(e) =>
        setProfileData({ ...profileData, oldPassword: e.target.value })
      }
      sx={{
        "& .MuiInputBase-root": {
          fontSize: "14px",
          borderRadius: "10px",
        },
        "& .MuiInputLabel-root": {
          fontSize: "13px",
        },
      }}
    />

    <TextField
      label="New Password"
      type="password"
      size="small"
      value={profileData.newPassword}
      onChange={(e) =>
        setProfileData({ ...profileData, newPassword: e.target.value })
      }
      sx={{
        "& .MuiInputBase-root": {
          fontSize: "14px",
          borderRadius: "10px",
        },
        "& .MuiInputLabel-root": {
          fontSize: "13px",
        },
      }}
    />

    </DialogContent>

    <DialogActions sx={{ px: 3, pb: 2 }}>
      <Button
        onClick={() => setOpenProfile(false)}
        variant="outlined"
        size="small"
        sx={{
          borderRadius: "10px",
          textTransform: "none",
        }}
      >
      Cancel
    </Button>

    <Button
      variant="contained"
      size="small"
      disabled={updateProfileMutation.isPending}
      onClick={() => {
        const body = {};

        if (profileData.name) body.name = profileData.name;
        if (profileData.oldPassword && profileData.newPassword) {
          body.old_password = profileData.oldPassword;
          body.new_password = profileData.newPassword;
        }

        updateProfileMutation.mutate(body);
      }}
      sx={{
        borderRadius: "10px",
        textTransform: "none",
        px: 3,
        boxShadow: "none",
        "&:hover": {
          boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
        },
      }}
    >
     {updateProfileMutation.isPending ? "Saving..." : "Save"}
    </Button>
    </DialogActions>
    </Dialog>
        </>
    );
}