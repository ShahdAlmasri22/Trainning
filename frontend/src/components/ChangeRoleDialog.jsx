import {
    Box,
    Button, Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControl,
    InputLabel,
    MenuItem,
    Select
} from "@mui/material";

export default function ChangeRoleDialog(
    {
        openRoleDialog,
        handleClose,
        setOpenRoleDialog,
        newRole,
        handleUpdateRole,
        setNewRole,
        updateRoleMutation,

    }
){
    return(
        <Box>

       <Dialog
          open={openRoleDialog}
          onClose={handleClose}
          PaperProps={{
            sx: {
              width: "400px",
              borderRadius: 3,
              p: 1,
            },
          }}
      >

      <DialogTitle sx={{display: "flex", justifyContent: "space-between", lignItems: "center", fontWeight: "bold", }}>
        Change User Role
          <Button
        onClick={() => setOpenRoleDialog(false)}
        sx={{
          minWidth: 0,
          color: "gray",
          fontSize: "13px",
        }}
      >
        ✕
      </Button>
      </DialogTitle>

      <DialogContent sx={{ mt: 1, overflow: "visible" }}>
        <FormControl fullWidth size="small">
          <InputLabel id="role-label">Role</InputLabel>

          <Select
            labelId="role-label"
            value={newRole}
            label="Role"

            onChange={(e) => setNewRole(e.target.value)}
            sx={{
              mt: 1,
            }}
          >
            <MenuItem value="USER">USER</MenuItem>
            <MenuItem value="ADMIN">ADMIN</MenuItem>
          </Select>
        </FormControl>
      </DialogContent>

      <DialogActions sx={{ justifyContent: "center", pb: 2, mt:2 }}>
        <Button onClick={handleClose} variant="outlined" size="small">
          Cancel
        </Button>

        <Button variant="contained" onClick={handleUpdateRole}
                size="small"
        disabled={updateRoleMutation.isPending}
        >
          {updateRoleMutation.isPending ? "Updating..." : "Confirm"}
        </Button>
       </DialogActions>
      </Dialog>

        </Box>
    );
}