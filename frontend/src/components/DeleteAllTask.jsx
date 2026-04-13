import {DialogTitle, Dialog, Button, DialogContent, DialogActions} from "@mui/material";


export default function DeleteAllTask(
    {
        openDeleteAll,
        setOpenDeleteAll,
        confirmDeleteAll,
        deleteAllMutation
    }
){
    return(
        <>
        <Dialog
          open={openDeleteAll}
          onClose={() => setOpenDeleteAll(false)}
        >
          <DialogTitle
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            Delete All Tasks

            <Button
              onClick={() => setOpenDeleteAll(false)}
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
            Are you sure you want to delete ALL tasks?
          </DialogContent>

          <DialogActions>
            <Button onClick={() => setOpenDeleteAll(false)}>
              Cancel
            </Button>

            <Button
              color="error"
              onClick={confirmDeleteAll}
              disabled={deleteAllMutation.isPending}
            >
              {deleteAllMutation.isPending ? "Deleting..." : "Delete"}
            </Button>
          </DialogActions>
        </Dialog>
        </>
    );
}
