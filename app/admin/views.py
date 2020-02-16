from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import ParticipantForm, StorageForm
from .. import db
from ..models import Participant, Storage

max_capacity=50

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Participant View

@admin.route('/participants', methods=['GET', 'POST'])
@login_required
def list_participants():
    """
    List all participants
    """
    check_admin()

    participants = Participant.query.all()

    return render_template('admin/participants/participants.html',
                           participants=participants, title="Participants")

@admin.route('/participants/add', methods=['GET', 'POST'])
@login_required
def add_participant():
    """
    Add a participant to the database
    """
    check_admin()

    add_participant = True

    form = ParticipantForm()
    if form.validate_on_submit():
        participant = Participant(partname=form.partname.data,
                                  fcd = float(form.fcd.data),
                                  usd = float(form.usd.data),
                                  sar = float(form.sar.data),
                                  rub = float(form.rub.data),
                                  yen = float(form.yen.data))
        try:
            # add participant to the database
            db.session.add(participant)
            db.session.commit()
            flash('You have successfully added a new participant.')
        except:
            # in case participant name already exists
            flash('Error: participant name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_participants'))

    # load department template
    return render_template('admin/participants/participant.html', action="Add",
                           add_participant=add_participant, form=form,
                           title="Add Participant")


@admin.route('/participants/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_participant(id):
    """
    Edit a participant
    """
    check_admin()

    add_participant = False

    participant = Participant.query.get_or_404(id)
    form = ParticipantForm(obj=participant)
    if form.validate_on_submit():
        participant.partname = form.partname.data
        participant.fcd = eval( "".join( form.fcd.data.split(",") ) ) 
        participant.usd = eval( "".join( form.usd.data.split(",") ) )
        participant.sar = eval( "".join( form.sar.data.split(",") ) )
        participant.rub = eval( "".join( form.rub.data.split(",") ) )
        participant.yen = eval( "".join( form.yen.data.split(",") ) )
        db.session.commit()
        flash('You have successfully edited the participant.')

        # redirect to the departments page
        return redirect(url_for('admin.list_participants'))

    form.yen.data = participant.yen
    form.rub.data = participant.rub
    form.sar.data = participant.sar
    form.usd.data = participant.usd
    form.fcd.data = participant.fcd
    form.partname.data = participant.partname
    return render_template('admin/participants/participant.html', action="Edit",
                           add_participant=add_participant, form=form,
                           participant=participant, title="Edit Participant")


@admin.route('/participants/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_participant(id):
    """
    Delete a participant from the database
    """
    check_admin()

    participant = Participant.query.get_or_404(id)
    db.session.delete(participant)
    db.session.commit()
    flash('You have successfully deleted the participant.')

    # redirect to the departments page
    return redirect(url_for('admin.list_participants'))

    return render_template(title="Delete Participant")

@admin.route('/storages')
@login_required
def list_storages():
    check_admin()
    """
    List all storages
    """
    storages = Storage.query.all()
    return render_template('admin/storages/storages.html',
                           storages=storages, title='Storages')

@admin.route('/storages/add', methods=['GET', 'POST'])
@login_required
def add_storage():
    """
    Add a storage to the database
    """
    check_admin()

    add_storage = True

    form = StorageForm()
    if form.validate_on_submit():
        if(form.current_capacity.data>max_capacity*form.stornum.data):
            flash('Error: input exceeded maximum capacity.')
        else:
            storage = Storage(storown=form.storown.data,
                            stornum=form.stornum.data,
                            current_capacity=form.current_capacity.data)

            try:
                # add storage to the database
                db.session.add(storage)
                db.session.commit()
                flash('You have successfully added a new storage.')
            except:
                # in case storage name already exists
                flash('Error: storage already exists.')

        # redirect to the storages page
        return redirect(url_for('admin.list_storages'))

    # load storage template
    return render_template('admin/storages/storage.html', add_storage=add_storage,
                           form=form, title='Add Storage')


@admin.route('/storages/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_storage(id):
    """
    Edit a storage
    """
    check_admin()

    add_storage = False

    storage = Storage.query.get_or_404(id)
    form = StorageForm(obj=storage)
    if form.validate_on_submit():
        if(form.current_capacity.data > form.stornum.data * max_capacity):
            flash('Error: input exceeded maximum capacity.')
        else:
            storage.storown = form.storown.data
            storage.stornum = form.stornum.data
            storage.current_capacity = form.current_capacity.data
            db.session.add(storage)
            db.session.commit()
            flash('You have successfully edited the storage.')

        # redirect to the storages page
        return redirect(url_for('admin.list_storages'))

    form.current_capacity.data = storage.current_capacity
    form.stornum.data = storage.stornum
    form.storown.data = storage.storown
    return render_template('admin/storages/storage.html', add_storage=add_storage,
                           form=form, title="Edit Storage")


@admin.route('/storages/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_storage(id):
    """
    Delete a storage from the database
    """
    check_admin()

    storage = Storage.query.get_or_404(id)
    db.session.delete(storage)
    db.session.commit()
    flash('You have successfully deleted the storage.')

    # redirect to the storages page
    return redirect(url_for('admin.list_storages'))

    return render_template(title="Delete Storage")