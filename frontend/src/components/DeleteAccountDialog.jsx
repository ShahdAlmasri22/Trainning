import {Button, Dialog, DialogActions, DialogContent, DialogTitle} from "@mui/material";

export default function DeleteAccountDialog (
    {
        deleteAcc,
        setDeleteAcc,
        deleteAccountMutation
    }
)
{
    return(
        <>
        <Dialog open={deleteAcc} onClose={() => setDeleteAcc(false)}>
            <DialogTitle sx={{ display: "flex", justifyContent: "space-between" }}>
              Delete Account

            <Button onClick={() => setDeleteAcc(false)} sx={{ minWidth: 0, color: "gray", fontSize: "13px", }}>
                ✕
            </Button>
            </DialogTitle>

            <DialogContent>
              Are you sure you want to delete your account?
            </DialogContent>

            <DialogActions>
            <Button onClick={() => setDeleteAcc(false)}>
              Cancel
            </Button>

            <Button
              color="error"
              disabled={deleteAccountMutation.isPending}
              onClick={() => {
                deleteAccountMutation.mutate();
              }}
            >
              {deleteAccountMutation.isPending ? "Deleting..." : "Delete"}
            </Button>
            </DialogActions>
            </Dialog>
        </>
    );
}