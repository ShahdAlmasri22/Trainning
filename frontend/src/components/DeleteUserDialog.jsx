import {Button, Dialog, DialogActions, DialogContent, DialogTitle} from "@mui/material";


export default function DeleteUserDialog(
    {
        openDeleteDialog,
        setOpenDeleteDialog,
        confirmDeleteUser,
        deleteUserMutation
    }
){
    return(
        <>
        <Dialog
          open={openDeleteDialog}
          onClose={() => setOpenDeleteDialog(false)}
        >
          <DialogTitle  sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
          >Delete User

            <Button
            onClick={() => setOpenDeleteDialog(false)}
            sx={{
              minWidth: 0,
              color: "gray",
              fontSize: "13px",
            }}
            >
             ✕
            </Button>

          </DialogTitle>

        <DialogContent>
          Are you sure you want to delete this user?
        </DialogContent>

        <DialogActions>
            <Button onClick={() => setOpenDeleteDialog(false)}>
              Cancel
            </Button>

            <Button
              color="error"
              onClick={confirmDeleteUser}
              disabled={deleteUserMutation.isPending}
            >
                {deleteUserMutation.isPending ? "Deleting..." : "Delete"}
            </Button>
        </DialogActions>
    </Dialog>
</>
    );

}
